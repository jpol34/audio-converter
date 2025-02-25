"""
Module for audio conversion tasks.

This module defines functions to convert audio files using FFmpeg and to
handle the overall conversion process, including creating a ZIP archive of
the converted files.
"""

import os
import subprocess
import shutil
import time
import zipfile
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils import get_ffmpeg_paths


def convert_file(ffmpeg_path, input_path, output_path):
    """Converts a single file using FFmpeg."""
    try:
        file_size_before = Path(input_path).stat().st_size
        ffmpeg_command = [
            ffmpeg_path, "-i", input_path, "-acodec", "pcm_mulaw",
            "-ar", "8000", "-ac", "1", output_path
        ]
        subprocess.run(
            ffmpeg_command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        file_size_after = Path(output_path).stat().st_size
        return "success", file_size_before, file_size_after
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "failed", 0, 0


def run_conversion(selected_files, update_progress, update_status):  \
        # pylint: disable=too-many-locals
    """Handles the overall conversion process."""
    ffmpeg_path, _ = get_ffmpeg_paths()
    if not ffmpeg_path:
        update_status(
            "❌ FFmpeg not found. Ensure the 'ffmpeg' folder is in the correct "
            "location.", "danger"
        )
        return None

    input_folder = Path(selected_files[0]).parent
    output_folder = input_folder / "converted"

    # Ensure "converted" folder is deleted before starting
    if output_folder.exists():
        shutil.rmtree(output_folder)
    output_folder.mkdir()

    # Delete existing ZIP file if it exists
    zip_file_path = input_folder / "converted_files.zip"
    if zip_file_path.exists():
        zip_file_path.unlink()

    total_files = len(selected_files)
    converted_count = 0
    failed_count = 0
    total_size_before = 0
    total_size_after = 0
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        futures = {
            executor.submit(
                convert_file,
                ffmpeg_path,
                file,
                str(output_folder / (Path(file).stem + ".wav"))
            ): file for file in selected_files
        }

        for i, future in enumerate(as_completed(futures)):
            result, size_before, size_after = future.result()
            if result == "success":
                converted_count += 1
                total_size_before += size_before
                total_size_after += size_after
            else:
                failed_count += 1

            # Update progress bar on every iteration
            update_progress(i + 1)

    # Ensure progress bar is fully updated
    update_progress(total_files)

    # Create ZIP file for converted files
    with zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file in output_folder.iterdir():
            zipf.write(file, file.name)

    elapsed_time = round(time.time() - start_time, 2)
    size_reduction_mb = (
        round((total_size_before - total_size_after) / (1024 * 1024), 2)
        if total_size_before else 0
    )

    # Return summary details
    return {
        "converted": converted_count,
        "failed": failed_count,
        "zip_path": zip_file_path,
        "size_reduction_mb": size_reduction_mb,
        "elapsed_time": elapsed_time
    }
