
import os
import sys


repo_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, repo_dir)
original_modules = sys.modules.copy()

modules_used = [
    "modules.separate",
    "modules.stft",
]
original_webui_modules = {}
for module in modules_used:
    if module in sys.modules:
        original_webui_modules[module] = sys.modules.pop(module)

from .nodes import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]