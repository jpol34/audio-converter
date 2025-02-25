"""
GUI module for the Audio Converter application.

This module defines the AudioConverterApp class which provides the main GUI,
including file selection, progress updates during conversion, and a summary 
display when conversion is complete.
"""

import threading
from pathlib import Path
from tkinter import filedialog

import ttkbootstrap as ttk
from conversion import run_conversion
from utils import format_time


class AudioConverterApp:  # pylint: disable=too-many-instance-attributes, too-few-public-methods
    """
    AudioConverterApp provides a GUI for converting audio files using FFmpeg.
    
    It allows users to select audio files, start the conversion process in a 
    background thread, and displays progress and conversion results.
    """
    def __init__(self, root):
        """
        Initialize the AudioConverterApp with the given root window.

        Args:
            root (ttk.Window): The root window for the application.
        """
        self.root = root
        self.root.title("Audio Converter")
        self.root.geometry("700x420")

        # Progress Bar
        self.progress = ttk.Progressbar(
            root, orient=ttk.HORIZONTAL, mode="determinate", length=600,
            bootstyle="info"
        )
        self.progress.pack(pady=10, padx=20)

        # Folder Selection Feedback
        self.folder_label = ttk.Label(
            root, text="No folder selected.", font=("Arial", 10),
            bootstyle="secondary"
        )
        self.folder_label.pack(pady=2)

        # Status Message
        self.status_label = ttk.Label(
            root, text="Select audio files to begin.", font=("Arial", 11),
            bootstyle="secondary"
        )
        self.status_label.pack(pady=5)

        # Button Frame
        button_frame = ttk.Frame(root)
        button_frame.pack(pady=10)

        self.select_folder_button = ttk.Button(
            button_frame, text="Select Files", command=self.select_files,
            bootstyle="secondary", width=15
        )
        self.select_folder_button.grid(row=0, column=0, padx=10)

        self.convert_button = ttk.Button(
            button_frame, text="Start Conversion", 
            command=self.start_conversion_thread, bootstyle="success",
            width=15
        )
        self.convert_button.grid(row=0, column=1, padx=10)

        self.exit_button = ttk.Button(
            button_frame, text="Exit", command=root.quit, bootstyle="danger",
            width=15
        )
        self.exit_button.grid(row=0, column=2, padx=10)

        # Summary Display Area
        self.summary_frame = ttk.Frame(root)
        self.summary_frame.pack(pady=10, fill="x", padx=20)

        self.summary_label = ttk.Label(
            self.summary_frame, text="", font=("Arial", 10), bootstyle="light"
        )
        self.summary_label.pack(pady=5)

        self.selected_files = []

    def select_files(self):
        """
        Allows the user to select multiple audio files and updates the folder 
        label with the selected folder path.
        """
        filetypes = [("Audio Files", "*.wav;*.m4a;*.aac;*.mp3"), ("All Files", "*.*")]
        files = filedialog.askopenfilenames(
            title="Select Audio Files", filetypes=filetypes
        )
        if files:
            self.selected_files = files
            folder_path = str(Path(files[0]).parent)
            self.folder_label.config(
                text=f"📂 Selected: {folder_path}", bootstyle="info"
            )

    def update_status(self, message, style="secondary"):
        """
        Updates the status label in a thread-safe way.

        Args:
            message (str): The status message to display.
            style (str): The bootstyle for the label.
        """
        self.root.after(
            0, lambda: self.status_label.config(text=message, bootstyle=style)
        )

    def update_progress(self, value):
        """
        Updates the progress bar in a thread-safe way.

        Args:
            value (int): The new value for the progress bar.
        """
        self.root.after(0, lambda: self.progress.config(value=value))
        self.root.after(0, self.root.update_idletasks)

    def display_summary(self, summary):
        """
        Displays the conversion summary in the GUI.

        Args:
            summary (dict): A dictionary containing conversion results.
        """
        formatted_time = format_time(summary["elapsed_time"])
        summary_text = (
            f"✅ Conversion Complete!\n"
            f"🎵 Files Converted: {summary['converted']}\n"
            f"⚠️ Failed: {summary['failed']}\n"
            f"📦 ZIP File: {summary['zip_path']}\n"
            f"📉 Size Reduction: {summary['size_reduction_mb']} MB\n"
            f"⏱️ Time Taken: {formatted_time}"
        )
        self.root.after(
            0, lambda: self.summary_label.config(text=summary_text, bootstyle="info")
        )

    def start_conversion_thread(self):
        """
        Starts the audio conversion process in a background thread.
        """
        if not self.selected_files:
            self.update_status("⚠️ Please select audio files first.", "warning")
            return

        # Set up the progress bar: value=0, maximum equals the number of files
        self.root.after(
            0, lambda: self.progress.config(
                value=0, maximum=len(self.selected_files)
            )
        )
        self.update_status("⏳ Conversion in progress...", "info")

        # Create thread-safe wrappers for status and progress updates.
        def thread_safe_update_progress(value):
            self.update_progress(value)

        def thread_safe_update_status(message, style="secondary"):
            self.update_status(message, style)

        # Run conversion in a separate thread.
        thread = threading.Thread(
            target=self.run_conversion_in_background,
            args=(thread_safe_update_progress, thread_safe_update_status)
        )
        thread.start()

    def run_conversion_in_background(self, update_progress, update_status):
        """
        Runs the conversion process in a background thread and updates the GUI
        upon completion.

        Args:
            update_progress (callable): Function to update the progress bar.
            update_status (callable): Function to update the status messages.
        """
        summary = run_conversion(
            self.selected_files, update_progress, update_status
        )
        if summary:
            self.root.after(0, lambda: self.display_summary(summary))
            self.root.after(
                0, lambda: self.update_status(
                    "✅ Conversion complete. Files zipped!", "success"
                )
            )
