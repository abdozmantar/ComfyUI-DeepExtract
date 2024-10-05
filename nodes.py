import logging
from .scripts.vocal_and_sound_remover import VocalAndSoundRemover

logger = logging.getLogger(__name__)

class VocalAndSoundRemoverNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_sound": ("AUDIO",),
            }
        }

    RETURN_TYPES = ("AUDIO","AUDIO",)
    RETURN_NAMES = ("Vocals","Background",)
    FUNCTION = "execute"
    CATEGORY = "DeepExtract"

    def execute(self, input_sound):
        vocal_remover = VocalAndSoundRemover(input_sound)
        
        vocals, background = vocal_remover.execute()

        return (vocals, background,)


NODE_CLASS_MAPPINGS = {
    "VocalAndSoundRemoverNode": VocalAndSoundRemoverNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "VocalAndSoundRemoverNode": "Vocal and Sound Separator",
}
