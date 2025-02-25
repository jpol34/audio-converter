"""
Main entry point for the Audio Converter application.

This module initializes the ttkbootstrap window and launches the AudioConverterApp.
"""

import ttkbootstrap as ttk
from gui import AudioConverterApp

if __name__ == "__main__":
    root = ttk.Window(themename="darkly")
    AudioConverterApp(root)
    root.mainloop()
