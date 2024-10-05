# DeepExtract 🎤

## Overview

**DeepExtract** is a powerful and efficient tool designed to separate vocals and sounds from audio files, providing an enhanced experience for musicians, producers, and audio engineers. With DeepExtract, you can quickly and effectively isolate vocals or instruments from mixed audio tracks, facilitating tasks like remixing, karaoke preparation, or audio analysis.

## Installation Guide 🛠️

Setting up **DeepExtract** is quick and straightforward! Simply follow the steps below to get started.

### Step 1: Clone the Repository

1. Clone this repository to your ComfyUI custom nodes folder. There is two way :

- A) Download this repository as a zip file and extract files in to `comfyui\custom_nodes\ComfyUI-DeepExtract` folder.

- B) Go to `comfyui\custom_nodes\` folder open a terminal window here and run `git clone https://github.com/abdozmantar/ComfyUI-DeepExtract` command.

### Step 2: Run the Setup Script

2. Go to `comfyui\custom_nodes\ComfyUI-DeepExtract` folder and open a terminal window and run `python setup.py` command. If you using windows you can double click `setup.bat` alternatively.

```bash
python setup.py
```

3. Wait patiently installation to finish.

4. Run the ComfyUI.

5. Double click anywhere in ComfyUI and search DeepExtract node by typing it or right click anywhere and select `Add Node > DeepExtract > VocalAndSoundRemoverNode` node to using it.

<img src="https://github.com/abdozmantar/ComfyUI-DeepExtract/blob/main/public/images/node_location.png?raw=true" alt="nodel location" width="100%"/>

##### OR

<img src="https://github.com/abdozmantar/ComfyUI-DeepExtract/blob/main/public/images/node_search.png?raw=true" alt="nodel location" width="100%"/>

## Usage

### How to Use the DeepExtract Node

To utilize the **DeepExtract** node, simply connect your audio input to the **VocalAndSoundRemoverNode**. Adjust the parameters to tailor the output to your needs. The node will process the audio and return isolated vocal and background tracks for further manipulation.

### Example Workflow

1. **Load an Audio File:** Begin by loading your mixed audio file into ComfyUI.
2. **Add the Node:** Insert the **VocalAndSoundRemoverNode** into your workflow.
3. **Connect Inputs and Outputs:** Link your audio source to the node and specify where to send the separated tracks.
4. **Process the Audio:** Execute the workflow to separate the vocals and sounds effectively.

## Structure

<img src="https://github.com/abdozmantar/ComfyUI-DeepExtract/blob/main/public/images/node_structure.png?raw=true" alt="nodel location" width="100%"/>

### Node Layout

The **DeepExtract** node features an intuitive interface that allows for easy manipulation. The input section accepts mixed audio files, while the output section provides two distinct tracks: one for isolated vocals and another for the background sounds. This design facilitates seamless integration into your audio processing workflow.

### Parameter Overview

- **Input Sound:** This is where you connect the mixed audio file.
- **Vocal Output:** This output provides the isolated vocal track.
- **Background Output:** This output delivers the remaining instrumental sound.

These additions, along with your original text, will create a clearer understanding of how to use the **DeepExtract** tool effectively!

## Contributing

We welcome contributions from the community! If you'd like to enhance DeepExtract, please fork the repository and submit a pull request.

### Guidelines

1. Fork the project.
2. Create a feature branch.
3. Commit your changes.
4. Push to the branch.
5. Submit a pull request.

### Author

👤 **Abdullah Ozmantar**  
[GitHub Profile](https://github.com/comfyui-abdozmantar)

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/abdozmantar/comfyui-deepextract/blob/main/LICENSE) file for details.
