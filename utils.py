"""
Utility functions for the Audio Converter application.

This module provides helper functions to locate FFmpeg executables and to
format time durations in a human-readable format.
"""

import sys
from pathlib import Path

def get_ffmpeg_paths():
    """
    Retrieve the paths to the ffmpeg and ffprobe executables.

    Returns:
        tuple: A tuple (ffmpeg_exec, ffprobe_exec) where each is a string
        representing the path to the executable if found; otherwise, (None, None).
    """
    exe_dir = Path(getattr(sys, '_MEIPASS', Path(__file__).parent))
    ffmpeg_dir = exe_dir / "ffmpeg" / "bin"

    ffmpeg_exec = ffmpeg_dir / "ffmpeg.exe"
    ffprobe_exec = ffmpeg_dir / "ffprobe.exe"

    if ffmpeg_exec.exists() and ffprobe_exec.exists():
        return str(ffmpeg_exec), str(ffprobe_exec)
    return None, None

def format_time(seconds):
    """
    Convert a time duration in seconds to a formatted string "Xm Ys".

    Args:
        seconds (float): The duration in seconds.

    Returns:
        str: The formatted time string.
    """
    if seconds < 60:
        return f"{seconds:.1f}s"
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes}m {seconds}s"
