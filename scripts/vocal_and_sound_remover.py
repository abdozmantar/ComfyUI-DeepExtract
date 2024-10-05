import logging
import os
import urllib.request

from modules.separate import (
    SeparateMDX
)

logger = logging.getLogger(__name__)

class ModelData:

    def __init__(self, model_name: str, download_url: str = "https://github.com/facefusion/facefusion-assets/releases/download/models-3.0.0/kim_vocal_2.onnx"):
        self.model_name = model_name
        self.model_path = self.get_model_path()
        self.model_basename = os.path.splitext(
            os.path.basename(self.model_path))[0]
        self.compensate = 1.009
        self.mdx_dim_f_set = 3072
        self.mdx_dim_t_set = 8
        self.mdx_n_fft_scale_set = 6144
        self.primary_stem = 'Vocals'

        self.mdx_segment_size = 256
        self.mdx_batch_size = 1

        if not os.path.exists(self.model_path) and download_url:
            print(f"Model not found, downloading: {download_url}")
            self.download_model(download_url)

    def get_model_path(self):
        script_dir = os.path.dirname(os.path.realpath(__file__))
        model_path = os.path.join(os.path.dirname(script_dir), 'models', self.model_name)
        return model_path
    
    def download_model(self, url: str):
        try:
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            urllib.request.urlretrieve(url, self.model_path)
            print(f"Model downloaded successfully: {self.model_path}")
        except Exception as e:
            raise Exception(f"An error occurred while downloading the model: {e}")
        
class VocalAndSoundRemover:

    def __init__(self, input_file, model_name='Kim_Vocal_2.onnx'):
        self.input_file = input_file
        self.model_name = model_name

    def execute(self):
        try:
            logger.info("Starting vocal and sound separation process.")

            process_data = {'audio_file': self.input_file }
            model = ModelData(self.model_name)

            logger.info("Model loaded successfully, starting separation.")
            separator = SeparateMDX(model, process_data)
            result = separator.separate()

            logger.info("Separation process completed successfully.")
            return result

        except Exception as e:
            logger.error(f"Error during separation: {str(e)}")
            raise e
