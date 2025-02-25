import os
import subprocess
import shutil
import sys
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog
from pathlib import Path
import time
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_ffmpeg_paths():
    exe_dir = Path(getattr(sys, '_MEIPASS', Path(__file__).parent))  
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
        self.root.geometry("700x420")  

        # Progress Bar
        self.progress = ttk.Progressbar(root, orient=HORIZONTAL, mode="determinate", length=600, bootstyle="info")
        self.progress.pack(pady=10, padx=20)

        # Folder Selection Feedback
        self.folder_label = ttk.Label(root, text="No folder selected.", font=("Arial", 10), bootstyle="secondary")
        self.folder_label.pack(pady=2)

        # Status Message
        self.status_label = ttk.Label(root, text="Select audio files to begin.", font=("Arial", 11), bootstyle="secondary")
        self.status_label.pack(pady=5)

        # Button Frame
        button_frame = ttk.Frame(root)
        button_frame.pack(pady=10)
        
        self.select_folder_button = ttk.Button(button_frame, text="Select Files", command=self.select_files, bootstyle="secondary", width=15)
        self.select_folder_button.grid(row=0, column=0, padx=10)
        
        self.convert_button = ttk.Button(button_frame, text="Start Conversion", command=self.run_conversion, bootstyle="success", width=15)
        self.convert_button.grid(row=0, column=1, padx=10)
        
        self.exit_button = ttk.Button(button_frame, text="Exit", command=root.quit, bootstyle="danger", width=15)
        self.exit_button.grid(row=0, column=2, padx=10)

        # Summary Display Area
        self.summary_frame = ttk.Frame(root)
        self.summary_frame.pack(pady=10, fill="x", padx=20)

        self.summary_label = ttk.Label(self.summary_frame, text="", font=("Arial", 10), bootstyle="light")
        self.summary_label.pack(pady=5)

        self.selected_files = []  

    def select_files(self):
        """ Allows user to select multiple audio files and extracts their folder path. """
        filetypes = [("Audio Files", "*.wav;*.m4a;*.aac;*.mp3"), ("All Files", "*.*")]
        files = filedialog.askopenfilenames(title="Select Audio Files", filetypes=filetypes)

        if files:
            self.selected_files = files
            folder_path = str(Path(files[0]).parent)  
            self.folder_label.config(text=f"📂 Selected: {folder_path}", bootstyle="info")

    def update_status(self, message, style="secondary"):
        """ Updates the status label. """
        self.status_label.config(text=message, bootstyle=style)
        self.root.update_idletasks()

    def format_time(self, seconds):
        """ Converts seconds to 'Xm Ys' format. """
        if seconds < 60:
            return f"{seconds:.1f}s"
        else:
            minutes = int(seconds // 60)
            seconds = int(seconds % 60)
            return f"{minutes}m {seconds}s"

    def display_summary(self, converted, failed, zip_path, size_reduction_mb, elapsed_time):
        """ Displays the summary inside the app. """
        formatted_time = self.format_time(elapsed_time)
        summary_text = (
            f"✅ Conversion Complete!\n"
            f"🎵 Files Converted: {converted}\n"
            f"⚠️ Failed: {failed}\n"
            f"📦 ZIP File: {zip_path}\n"
            f"📉 Size Reduction: {size_reduction_mb} MB\n"
            f"⏱️ Time Taken: {formatted_time}"
        )
        self.summary_label.config(text=summary_text, bootstyle="info")

    def convert_file(self, ffmpeg_path, input_path, output_path):
        """ Converts a single file using FFmpeg. """
        try:
            file_size_before = Path(input_path).stat().st_size
            ffmpeg_command = [ffmpeg_path, "-i", input_path, "-acodec", "pcm_mulaw", "-ar", "8000", "-ac", "1", output_path]
            subprocess.run(ffmpeg_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
            file_size_after = Path(output_path).stat().st_size
            return "success", file_size_before, file_size_after
        except Exception:
            return "failed", 0, 0

    def run_conversion(self):
        """ Runs the audio conversion process. """
        if not self.selected_files:
            self.update_status("⚠️ Please select audio files first.", "warning")
            return

        self.update_status("⏳ Conversion in progress...", "info")

        ffmpeg_path, _ = get_ffmpeg_paths()
        if not ffmpeg_path:
            self.update_status("❌ FFmpeg not found. Ensure the 'ffmpeg' folder is in the correct location.", "danger")
            return

        input_folder = Path(self.selected_files[0]).parent  
        output_folder = input_folder / "converted"

        # Ensure "converted" folder is deleted before starting
        if output_folder.exists():
            shutil.rmtree(output_folder)
        output_folder.mkdir()

        # Delete existing ZIP file if it exists
        zip_file_path = input_folder / "converted_files.zip"
        if zip_file_path.exists():
            zip_file_path.unlink()

        total_files = len(self.selected_files)
        self.progress["value"] = 0
        self.progress["maximum"] = total_files

        start_time = time.time()
        converted_count = 0
        failed_count = 0
        total_size_before = 0
        total_size_after = 0

        with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
            futures = {
                executor.submit(self.convert_file, ffmpeg_path, file, str(output_folder / (Path(file).stem + ".wav"))): file
                for file in self.selected_files
            }

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

        # Create ZIP file for converted files
        with zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for file in output_folder.iterdir():
                zipf.write(file, file.name)

        elapsed_time = round(time.time() - start_time, 2)
        size_reduction_mb = round((total_size_before - total_size_after) / (1024 * 1024), 2) if total_size_before else 0

        self.display_summary(converted_count, failed_count, zip_file_path, size_reduction_mb, elapsed_time)
        self.update_status("✅ Conversion complete. Files zipped!", "success")

if __name__ == "__main__":
    root = ttk.Window(themename="darkly")
    app = AudioConverterApp(root)
    root.mainloop()
