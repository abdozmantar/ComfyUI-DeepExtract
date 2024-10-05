from __future__ import annotations
from typing import TYPE_CHECKING
import os
import gc
import logging
import numpy as np
import soundfile as sf
import librosa
import torch
import onnxruntime
from onnx import load
from onnx2pytorch import ConvertModel

from .stft import STFT

if TYPE_CHECKING:
    from scripts.vocal_and_sound_remover import ModelData

logger = logging.getLogger(__name__)

def clear_gpu_cache():
    gc.collect()
    torch.cuda.empty_cache()


def verify_audio(audio_file):
    is_audio = True

    if not type(audio_file) is tuple:
        audio_file = [audio_file]

    for i in audio_file:
        if os.path.isfile(i):
            try:
                librosa.load(i, duration=3, mono=False, sr=44100)
            except Exception as e:
                print(f'Failed to load {audio_file}: {e}')
                is_audio = False

    return is_audio


    """ def prepare_mix(mix):
    if not isinstance(mix, np.ndarray):
        mix, sr = librosa.load(mix, mono=False, sr=44100)
    else:
        mix = mix.T

    if mix.ndim == 1:
        mix = np.asfortranarray([mix, mix])

    return mix """

def prepare_mix(mix):
    if isinstance(mix, dict) and 'waveform' in mix and 'sample_rate' in mix:
        mix = mix['waveform'].numpy()
    if mix.ndim == 3 and mix.shape[0] == 1:
        mix = np.squeeze(mix, axis=0)

    if mix.ndim == 1:
        mix = np.asfortranarray([mix, mix])
    return mix


class SeparateAttributes:

    def __init__(self, model_data: ModelData, process_data: dict):
        self.model_basename = model_data.model_basename
        self.model_path = model_data.model_path
        self.primary_stem = model_data.primary_stem
        self.mdx_segment_size = model_data.mdx_segment_size
        self.mdx_batch_size = model_data.mdx_batch_size
        self.compensate = model_data.compensate
        self.dim_f = model_data.mdx_dim_f_set
        self.dim_t = 2**model_data.mdx_dim_t_set
        self.n_fft = model_data.mdx_n_fft_scale_set
        self.hop = 1024
        self.adjust = 1
        self.audio_file = process_data['audio_file']
        self.device = torch.device(
            'cuda' if torch.cuda.is_available() else 'cpu')
        self.run_type = ['CUDAExecutionProvider'] if torch.cuda.is_available() else [
            'CPUExecutionProvider']


class SeparateMDX(SeparateAttributes):

    def separate(self):
        samplerate = 44100

        if self.mdx_segment_size == self.dim_t:
            ort_ = onnxruntime.InferenceSession(
                self.model_path, providers=self.run_type)
            self.model_run = lambda spek: ort_.run(
                None, {'input': spek.cpu().numpy()})[0]
        else:
            self.model_run = ConvertModel(load(self.model_path))
            self.model_run.to(self.device).eval()
        
        mix = prepare_mix(self.audio_file)

        logger.info(mix)
        logger.info(mix.shape)

        vocals = self.demix(mix)

        background = mix - vocals


        clear_gpu_cache()

        vocals_tensor = torch.tensor(vocals, dtype=torch.float32).unsqueeze(0)
        background_tensor = torch.tensor(background, dtype=torch.float32).unsqueeze(0)
    
        
        logger.info(vocals_tensor.shape)
        logger.info(background_tensor.shape)

        return {'waveform': vocals_tensor, 'sample_rate': 44100}, {'waveform': background_tensor, 'sample_rate': 44100}

    def initialize_model_settings(self):
        self.n_bins = self.n_fft//2+1
        self.trim = self.n_fft//2
        self.chunk_size = self.hop * (self.mdx_segment_size-1)
        self.gen_size = self.chunk_size-2*self.trim
        self.stft = STFT(self.n_fft, self.hop, self.dim_f, self.device)

    def demix(self, mix):
        self.initialize_model_settings()

        tar_waves_ = []

        chunk_size = self.chunk_size

        gen_size = chunk_size-2*self.trim

        pad = gen_size + self.trim - ((mix.shape[-1]) % gen_size)
        mixture = np.concatenate((np.zeros(
            (2, self.trim), dtype='float32'), mix, np.zeros((2, pad), dtype='float32')), 1)

        step = self.chunk_size - self.n_fft
        result = np.zeros((1, 2, mixture.shape[-1]), dtype=np.float32)
        divider = np.zeros((1, 2, mixture.shape[-1]), dtype=np.float32)
        total = 0

        for i in range(0, mixture.shape[-1], step):
            total += 1
            start = i
            end = min(i + chunk_size, mixture.shape[-1])

            chunk_size_actual = end - start

            window = np.hanning(chunk_size_actual)
            window = np.tile(window[None, None, :], (1, 2, 1))

            mix_part_ = mixture[:, start:end]
            if end != i + chunk_size:
                pad_size = (i + chunk_size) - end
                mix_part_ = np.concatenate(
                    (mix_part_, np.zeros((2, pad_size), dtype='float32')), axis=-1)

            mix_part = torch.tensor(
                mix_part_, dtype=torch.float32).unsqueeze(0).to(self.device)
            mix_waves = mix_part.split(self.mdx_batch_size)

            with torch.no_grad():
                for mix_wave in mix_waves:
                    tar_waves = self.run_model(mix_wave)

                    tar_waves[..., :chunk_size_actual] *= window
                    divider[..., start:end] += window

                    result[..., start:end] += tar_waves[..., :end-start]

        epsilon = 2e-16  # Prevent division by 0 warning
        tar_waves = result / (divider + epsilon)
        tar_waves_.append(tar_waves)

        tar_waves_ = np.vstack(tar_waves_)[:, :, self.trim:-self.trim]
        tar_waves = np.concatenate(tar_waves_, axis=-1)[:, :mix.shape[-1]]

        source = tar_waves[:, 0:None]

        source = source * self.compensate

        return source

    def run_model(self, mix):
        spek = self.stft(mix.to(self.device))*self.adjust
        spek[:, :, :3, :] *= 0

        spec_pred = self.model_run(spek)

        return self.stft.inverse(torch.tensor(spec_pred).to(self.device)).cpu().detach().numpy()
