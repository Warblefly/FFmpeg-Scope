REM By John Warburton john@johnwarburton.net
REM Copyright (C) John Warburton 2014
REM
REM Licenced under the GNU GPL Version 3

REM Batch file to launch Python program scope.py
REM You will need to put your path to the directory containing the
REM Python executable in PYTHON_SCOPE_DIR
REM
REM Ensure the FFmpeg suite is in your path.
REM You will need ffplay and ffprobe
REM 
REM Execute this program by typing:
REM scope VIDEOFILE
REM
REM The Python script examines the "best" video track, and the "best" audio track
REM in the file you give it. It will fail if the file is missing one of these.
REM
REM This script is tested with stereo audio only.

SET PYTHON_SCOPE_DIR="C:\Program Files\ffmpeg\bin"

python %PYTHON_SCOPE_DIR%\scope.py %1

