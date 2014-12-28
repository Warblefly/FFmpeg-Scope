FFmpeg-Scope
============

Summary:

Video and audio scope for TV: waveform, vector, audio with broadcast level check
Video levels 16, 127 and 235 are shown.

Requirements:

Python 3.4.1
Recent FFmpeg suite, including ffmpeg, ffprobe, ffplay: compiled with SDL and most other options.
(Please see MultimediaWin64 for compiling these on a Windows platform)

Use:
scope VIDEOFILE
There are no options at present. The VIDEOFILE must have a picture track and a stereo audio track.
Any frame rate is acceptable.
Timecode always starts at 00:00:00:00

These files are released under the GNU GPL Version 3

Enquiries? john@johnwarburton.net
