# Audio Converter (CLI & GUI)

## 📌 Overview

This **Audio Converter** application allows you to convert multiple audio files to `.wav` format using **FFmpeg**. It supports both **Graphical User Interface (GUI)** and **Command-Line Interface (CLI)** modes, making it easy to use for all users.

✅ **Convert** `.wav`, `.m4a`, `.aac`, `.mp3` files into `.wav` ✅ **Batch Processing**: Convert an entire folder in one go ✅ **Multi-threaded Processing**: Faster conversion using multi-core processors ✅ **ZIP Output**: Saves all converted files in `converted_files.zip` ✅ **Progress Bar & Summary**: Available in both **GUI & CLI** modes ✅ **Standalone Executable**: Can be run without Python (after compilation)

---

## 🛠️ Installation & Requirements

### **1️⃣ Prerequisites**

- **Windows** (Tested on Windows 10/11)
- **Python 3.x** (if running the script directly)
- **FFmpeg** (included in the application directory)

### **2️⃣ Install Required Dependencies**

If running the script with Python, install required libraries:

```sh
pip install ttkbootstrap tqdm
```

---

## 🚀 Usage

### **1️⃣ Run GUI Mode**

If you want to use the graphical interface, simply **double-click** the executable (if compiled) or run:

```sh
python script.py
```

### **2️⃣ Run CLI Mode (Convert a Folder)**

To convert all audio files inside a folder **without using the GUI**, run:

```sh
python script.py -d "C:\path\to\audio_files"
```

Or, if using the **compiled EXE**:

```sh
audio_converter.exe -d "C:\path\to\audio_files"
```

**Example:**

```sh
python script.py -d "C:\Users\John\Music"
```

### **3️⃣ Example CLI Output**

```
⏳ Converting 5 files...
Processing: 100% |███████████████████████████████| 5/5 files
✅ Conversion Complete!
🎵 Files Converted: 5
⚠️ Failed: 0
📦 ZIP File: C:\Users\John\Music\converted_files.zip
📉 Size Reduction: 2.3 MB
⏱️ Time Taken: 10.5s
```

---

## 🎯 Features

### **✅ Graphical User Interface (GUI)**

- Select audio files manually
- Visual progress bar
- Displays summary after conversion

### **✅ Command Line Interface (CLI)**

- Allows batch processing of an entire folder
- Uses `tqdm` to show a live progress bar
- Displays summary in the terminal

### **✅ Multi-threaded Processing**

- Uses `ThreadPoolExecutor` to **convert multiple files simultaneously**
- Faster than single-threaded conversion

### **✅ ZIP Packaging**

- All converted files are stored in a `` folder
- A `.zip` file (`converted_files.zip`) is automatically created

### **✅ FFmpeg Integration**

- Uses **FFmpeg** for high-quality audio conversion
- No need to install FFmpeg separately (included in the project)

---

## 🔧 Troubleshooting

### **1️⃣ CLI Mode Doesn’t Work?**

Try running:

```sh
python script.py --help
```

If `audio_converter.exe` is **not recognized**, navigate to its directory and run:

```sh
cd C:\path\to\exe
audio_converter.exe -d "C:\path\to\audio_files"
```

### **2️⃣ FFmpeg Not Found?**

If you see:

```
❌ FFmpeg not found. Ensure the 'ffmpeg' folder is in the correct location.
```

Make sure:

- The `ffmpeg` folder is **inside the application directory**
- The `ffmpeg/bin/` folder contains `ffmpeg.exe` and `ffprobe.exe`

### **3️⃣ Debugging Issues**

Run:

```sh
audio_converter.exe -d "C:\path\to\audio_files" > log.txt 2>&1
```

This will save all output to `log.txt` for debugging.

---

## 🏗️ Building an Executable (EXE)

If you want to **convert the script into a standalone EXE**, use **PyInstaller**:

```sh
pip install pyinstaller
pyinstaller --onefile --windowed --add-data "ffmpeg;ffmpeg" script.py
```

After building, your executable will be in the `dist/` folder.

---

## 📝 License

This project is **open-source** and free to use.

---

## 💡 Credits

- **FFmpeg**: Used for audio conversion
- **ttkbootstrap**: GUI styling
- **tqdm**: CLI progress bar

---

Now you can **convert your audio files easily with both GUI and CLI!** 🚀

