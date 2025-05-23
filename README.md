# yt-dlp simpleGUI

```markdown
__               __            ____    
\ \       __  __/ /_      ____/ / /___ 
 \ \     / / / / __/_____/ __  / / __ \
 / /    / /_/ / /_/_____/ /_/ / / /_/ /
/_/_____\__, /\__/      \__,_/_/ .___/ 
 /_____/____/     simple GUI  /_/
                           
```

Simple GUI to interact with the yt-dlp command-line downloader.

## How it works
This program dowloads the *yt-dlp* binary from [yt-dlp repositories](https://github.com/yt-dlp/yt-dlp) and interacts with it using a simple interface built using Python with `Tkinter`.

It can download MP3, FLAC and MP4 using pre-set flags, and also update the yt-dlp binary.

## Required Libraries:

- Tkinter (dev) for interface `(can be installed via pip/pipx)`
- urllib3 (dev) for downloading the yt-dlp binary `(can be installed via pip/pipx)`
- mutagen (or mutagenx fork) for metadata `(can be installed via pip/pipx or distro repo)`
- atomicparsley `(via distro repo)`
- ffmpeg `(via distro repo)`

## Installing in Windows
You will have to manually put the necessary files in the same folder of the program:

### FFmpeg
Windows builds of FFmpeg [here](https://ffmpeg.org/download.html)

- ffmpeg.exe
- fprobe.exe
- ffplay.exe

Or install it via `chocolatey` or `scoop`.

### AtomicParsley
Download via the [Github project page](https://github.com/wez/atomicparsley/releases).

## About Cookies
The flag `cookies-from-browser [browser name]` is used to fetch cookies from the specified browser in order to acess restricted content.

**Please note that you may have issues trying to use a browser with multiple profiles. In this case keep only one browser profile opened at a time.**

## Metadata
Metadata for audio files (artist name, album, etc) is done using [atomicparsley](https://github.com/wez/atomicparsley) and [mutagen](https://pypi.org/project/mutagen/).

On Linux you can get atomicparsley and mutagen from your package manager, or do the same as Windows (see above).

# Build Instructions

You can run it directly from the source (assuming that you have the required libraries) or build a executable with `pyinstaller`, avaliable via `pip`.

**Linux**

`pyinstaller --onefile yt-dlp_simpleGUI.py`

For seeing the shell messages, run it via terminal using `./yt-dlp_simpleGUI`

**Windows**

`pyinstaller --onefile yt-dlp_simpleGUI.py`

or `pyinstaller --onefile --hide-console hide-early yt-dlp_simpleGUI_Win.py` if you want to hide the command prompt.

*note: The program may hang when first downloading the yt-dlp binary on Windows, give a minute before doing another action*
