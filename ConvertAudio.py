import os
import subprocess
import shutil
import sys
import tkinter as tk
from tkinter import ttk, filedialog
from pathlib import Path
import time
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed

# Function to find FFmpeg in the specified directory
def get_ffmpeg_paths():
    exe_dir = Path(getattr(sys, '_MEIPASS', Path(__file__).parent))  # Support for PyInstaller
    ffmpeg_dir = exe_dir / "ffmpeg" / "bin"
    
    ffmpeg_exec = ffmpeg_dir / "ffmpeg.exe"
    ffprobe_exec = ffmpeg_dir / "ffprobe.exe"

    if ffmpeg_exec.exists() and ffprobe_exec.exists():
        return str(ffmpeg_exec), str(ffprobe_exec)
    
    return None, None

class AudioConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Converter")
        self.root.geometry("600x350")
        
        # Dynamically locate the icon file
        icon_path = Path(getattr(sys, '_MEIPASS', Path(__file__).parent)) / "icon.ico"
        if icon_path.exists():
            self.root.iconbitmap(str(icon_path))

        # Title Label
        self.status_label = tk.Label(root, text="Audio Converter", font=("Arial", 14, "bold"))
        self.status_label.pack(pady=10)

        # Progress Bar
        self.progress = ttk.Progressbar(root, orient=tk.HORIZONTAL, mode="determinate", length=500)
        self.progress.pack(pady=10, padx=20)

        # Status message area
        self.message_label = tk.Label(root, text="Select a folder to start conversion", font=("Arial", 12))
        self.message_label.pack(pady=5)

        # Button Frame
        button_frame = tk.Frame(root)
        button_frame.pack(pady=15)
        
        self.select_folder_button = tk.Button(button_frame, text="Select Folder", command=self.select_folder, font=("Arial", 11), width=15, height=2)
        self.select_folder_button.grid(row=0, column=0, padx=10)
        
        self.convert_button = tk.Button(button_frame, text="Start Conversion", command=self.run_conversion, font=("Arial", 11), width=15, height=2)
        self.convert_button.grid(row=0, column=1, padx=10)
        
        self.exit_button = tk.Button(button_frame, text="Exit", command=root.quit, font=("Arial", 11), width=15, height=2)
        self.exit_button.grid(row=0, column=2, padx=10)

        self.input_folder = None
    
    def select_folder(self):
        self.input_folder = filedialog.askdirectory(title="Select Input Folder")
        if self.input_folder:
            self.message_label.config(text=f"Selected Folder: {self.input_folder}")
    
    def log_message(self, message):
        self.message_label.config(text=message)
        self.root.update_idletasks()

    def convert_file(self, ffmpeg_path, input_path, output_path):
        try:
            file_size_before = Path(input_path).stat().st_size
            ffmpeg_command = [ffmpeg_path, "-i", input_path, "-acodec", "pcm_mulaw", "-ar", "8000", "-ac", "1", output_path]
            subprocess.run(ffmpeg_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
            file_size_after = Path(output_path).stat().st_size
            return "success", file_size_before, file_size_after
        except Exception:
            return "failed", 0, 0

    def run_conversion(self):
        if not self.input_folder:
            self.log_message("Please select an input folder first.")
            return

        self.log_message("Starting conversion process...")

        ffmpeg_path, _ = get_ffmpeg_paths()
        if not ffmpeg_path:
            self.log_message("FFmpeg not found. Please ensure the ffmpeg folder is in the correct location.")
            return

        input_folder = Path(self.input_folder)
        output_folder = input_folder / "converted"
        if output_folder.exists():
            shutil.rmtree(output_folder)
        output_folder.mkdir()

        audio_files = [f for f in input_folder.iterdir() if f.suffix.lower() in [".wav", ".m4a", ".aac", ".mp3"]]
        total_files = len(audio_files)
        if total_files == 0:
            self.log_message("No audio files found for conversion.")
            return

        self.progress["value"] = 0
        self.progress["maximum"] = total_files
        
        start_time = time.time()
        converted_count = 0
        failed_count = 0
        total_size_before = 0
        total_size_after = 0

        with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
            futures = {executor.submit(self.convert_file, ffmpeg_path, str(file), str(output_folder / (file.stem + ".wav"))): file for file in audio_files}

            for i, future in enumerate(as_completed(futures)):
                result, size_before, size_after = future.result()
                if result == "success":
                    converted_count += 1
                    total_size_before += size_before
                    total_size_after += size_after
                else:
                    failed_count += 1
                
                if i % 5 == 0 or i == total_files - 1:
                    self.progress["value"] = i + 1
                    self.root.update_idletasks()
        
        zip_file_path = input_folder / "converted_files.zip"
        with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in output_folder.iterdir():
                zipf.write(file, arcname=file.name)
        
        summary = f"Conversion Complete: {converted_count} files converted, {failed_count} failed.\nSaved to: {output_folder}\nZIP archive created at: {zip_file_path}"
        self.log_message(summary)

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioConverterApp(root)
    root.mainloop()
