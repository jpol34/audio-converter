# Audio Converter

## Overview
The **Audio Converter** is a desktop application that allows users to convert audio files to WAV format using FFmpeg. It supports multiple file selections, batch conversion, and compresses converted files into a ZIP archive for easy access. The application features a graphical user interface (GUI) built with `ttkbootstrap` for an enhanced user experience.

## Features
- **Batch conversion**: Convert multiple audio files simultaneously.
- **Supported formats**: WAV, M4A, AAC, MP3.
- **FFmpeg integration**: Uses FFmpeg for reliable and high-quality audio conversion.
- **Progress tracking**: Displays progress bar and status updates during conversion.
- **Automatic ZIP packaging**: Converted files are compressed into a ZIP archive.
- **Multithreading support**: Faster conversion using multiple CPU cores.

## Prerequisites
Ensure the following dependencies are installed before running the application:

- **Python 3.7+**
- **FFmpeg** (included in the `ffmpeg/bin` directory for distribution)
- Required Python packages:
  ```sh
  pip install ttkbootstrap
  ```

## Installation
1. Clone or download the repository.
2. Ensure `ffmpeg` is placed inside the application directory (`ffmpeg/bin/ffmpeg.exe`).
3. Install the required dependencies using:
   ```sh
   pip install -r requirements.txt
   ```

## Usage
1. **Run the application**:
   ```sh
   python audio_converter.py
   ```
2. **Select audio files** by clicking the **"Select Files"** button.
3. **Start conversion** by clicking the **"Start Conversion"** button.
4. The converted files will be stored in a `converted` folder inside the source directory.
5. A ZIP file (`converted_files.zip`) containing all converted files will be created.
6. View the summary and exit the application when done.

## Folder Structure
```
📂 audio_converter/
 ├── 📂 ffmpeg/
 │   ├── 📂 bin/
 │   │   ├── ffmpeg.exe
 │   │   ├── ffprobe.exe
 ├── audio_converter.py
 ├── requirements.txt
 ├── README.md
```

## Building an Executable (Windows)
To package the script into a standalone executable:
```sh
pip install pyinstaller
pyinstaller --noconsole --onefile --add-binary "ffmpeg/bin/ffmpeg.exe;ffmpeg/bin" --add-binary "ffmpeg/bin/ffprobe.exe;ffmpeg/bin" convertaudio.py
```
This creates an `audio_converter.exe` inside the `dist/` folder.

## Troubleshooting
- **FFmpeg not found**: Ensure the `ffmpeg/bin` directory exists and contains `ffmpeg.exe`.
- **No files selected**: Select files before clicking "Start Conversion".
- **Conversion fails**: Check if the audio files are supported.

## License
This project is licensed under the MIT License.

## Author
Developed by [Your Name]

