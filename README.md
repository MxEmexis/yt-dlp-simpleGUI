# yt-dlp simpleGUI
Simple GUI to interact with the yt-dlp command-line downloader.

## How it works
This program dowloads the *yt-dlp* binary from [yt-dlp repositories](https://github.com/yt-dlp/yt-dlp) and interacts with it using a simple interface built using Python with `Tkinter` and `urllib3` libraries.

I will add more features to it later, but at the moment it can download MP3 audio and MP4 video using pre-set flags, and also update the yt-dlp binary.

## Platforms
Windows and Linux, but with "Linux-first" philosophy in mind.

## Requirements:

- Tkinter via `pip install tk` (dev)
- urllib3 via `pip install urllib3` (dev) for downloading the yt-dlp binary
- ffmpeg

In Linux you can download `wget` from the repositories of your distro, FFmpeg should already be installed by default.

## Installing in Windows

### FFmpeg
You will have to manually put the necessary files in the same folder of the program:

Windows builds of FFmpeg [here](https://ffmpeg.org/download.html)

- ffmpeg.exe
- fprobe.exe
- ffplay.exe

Or install it via `chocolatey` or `scoop`.

## Build Instructions

Made via **pyinstaller** with `pip install pyinstaller`.

**Linux**

`pyinstaller --onefile yt-dlp_simpleGUI.py`

For seeing the shell messages, run it via terminal using `./yt-dlp_simpleGUI`

**Windows**

`pyinstaller --onefile yt-dlp_simpleGUI_Win.py`

or `pyinstaller --onefile --hide-console hide-early yt-dlp_simpleGUI_Win.py` if you want to hide the command prompt.

*note: The program may hang when first downloading the yt-dlp binary on Windows, give a minute before doing another action*
