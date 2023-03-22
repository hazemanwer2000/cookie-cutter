# cookie-cutter
A **PyQt6**-based video-editing graphical interface for **FFMPEG**.

* Trim an hour-long video in seconds, by cutting at keyframes.
* Mute audio in a few seconds, by removing all audio streams.
* Cut and combine video chunks with high accuracy, reaching milli-seconds.
* Generate *GIF*s, setting frame rate, playback speed, and dimensions.
* Apply filters, such as adjustable fade in and out.

<br>

<p align="center">
  <img src="https://github.com/hazemanwer2000/cookie-cutter/blob/main/snapshot.png" alt="A snapshot of Cookie Cutter' in action." width="800">
</p>

## Installation Requirements
Dependencies:
* Python modules: 
  * `python-vlc`
  * `pyqt6`
  * `pymediainfo`
* Binaries:
  * `ffmpeg`
  * `ffprobe`
  * `vlc`
    
#### Notes: 
  * Make sure `ffmpeg` and `ffprobe` reside in system path environment variable.
  * Execute `src/app.py -h` for help.
  * All configuration resides in `src/cc_constants.py`.
