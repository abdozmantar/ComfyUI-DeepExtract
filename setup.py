import warnings
import subprocess
import os
import sys
import urllib.request
try:
    from pkg_resources import get_distribution as distributions, version as pv
except:
    from importlib_metadata import distributions
from pathlib import Path
from tqdm import tqdm

# Suppress deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Display welcome message
print(f"\n")
print(f"-----------------------------------------------------------------")
print(f"🌟 Welcome to the DeepExtract Vocal and Sound Separator Installer 🌟")
print(f"-----------------------------------------------------------------")
print(f"\n")

# Define the models directory relative to the script's location
models_dir = os.path.join(Path(__file__).resolve().parent, "models")  # Kök dizinde models klasörü

# Create models directory if it doesn't exist
os.makedirs(models_dir, exist_ok=True)

# Define paths and URLs
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
req_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "requirements.txt")
model_url = "https://github.com/facefusion/facefusion-assets/releases/download/models-3.0.0/kim_vocal_2.onnx"
model_name = os.path.basename(model_url)
model_path = os.path.join(models_dir, model_name)  # Modelin tam yolu

print(model_path)

# Function to run pip install commands
def run_pip(*args):
    subprocess.run([sys.executable, '-m', 'pip', 'install', '--no-warn-script-location', *args])

# Function to check if a package is installed
def is_installed (
        package: str, version: str = None, strict: bool = True
):
    has_package = None
    try:
        has_package = distributions(package)
        if has_package is not None:
            if version is not None:
                installed_version = has_package.version
                if (installed_version != version and strict == True) or (pv.parse(installed_version) < pv.parse(version) and strict == False):
                    return False
                else:
                    return True
            else:
                return True
        else:
            return False
    except Exception as e:
        print(f"Status: {e}")
        return False

# Conditional installation for tqdm package
if not is_installed("tqdm"):
    print("🔧 INSTALLING: tqdm...")
    run_pip("tqdm")

# Function to download a file with progress bar
def download(url, path):
    request = urllib.request.urlopen(url)
    total = int(request.headers.get('Content-Length', 0))
    with tqdm(total=total, desc='Downloading', unit='B', unit_scale=True, unit_divisor=1024) as progress:
        urllib.request.urlretrieve(url, path, reporthook=lambda count, block_size, total_size: progress.update(block_size))

# Download the model if it doesn't exist
if not os.path.exists(model_path):
    print("📥 Downloading the model, please wait...")
    download(model_url, model_path)

# Install required packages
with open(req_file) as file:
    try:
        # Install onnxruntime-gpu package
        print("🔧 INSTALLING: onnxruntime-gpu...")
        run_pip("onnxruntime-gpu", "--extra-index-url", "https://aiinfra.pkgs.visualstudio.com/PublicPackages/_packaging/onnxruntime-cuda-11/pypi/simple/")
        
        # Install torch and related packages
        print("🔧 INSTALLING: torch, torchvision, torchaudio...")
        run_pip("torch", "torchvision", "torchaudio", "--extra-index-url", "https://download.pytorch.org/whl/cu118")

       

    except Exception as e:
        print(f"❌------------------------!ERROR!--------------------------------------")
        print(f"MODULE: onnxruntime-gpu")
        print(f"DeepExtract may not work.")
        print(f"ERROR: ")
        print(e)
        print(f"---------------------------------------------------------------------")
        raise e
    
    strict = True
    for package in file:
        package_version = None
        try:
            print(f"🔧 INSTALLING PACKAGE: {package.strip()}")
            package = package.strip()
            if "==" in package:
                package_version = package.split('==')[1]
            elif ">=" in package:
                package_version = package.split('>=')[1]
                strict = False
            
            if not is_installed(package, package_version, strict):
                run_pip(package)
        except Exception as e:
            print(f"❌------------------------!ERROR!--------------------------------------")
            print(f"MODULE: {package.strip()}")
            print(f"DeepExtract may not work.")
            print(f"ERROR: ")
            print(e)
            print(f"---------------------------------------------------------------------")
            raise e

print("\n")
print(f"🎉-----------------------------------------------------------------")
print(f"🎉 DeepExtract Installation completed successfully! 🎉")
print(f"🔄 Please restart your application to access the Vocal and Sound Separator node under DeepExtract in ComfyUI. 🔄")