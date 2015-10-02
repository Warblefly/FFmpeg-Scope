# scope.py (C) John Warburton 2014. john@johnwarburton.com
# Released under GPL version 3. http://gnu.org
# You may distribute and/or modify this code if you make available your changes under the same licence.
# Keeping your changes secret, or making them only available for pay is prohibited.
# You may offer paid support for anything you do with this code.
# You can even pay me to support your use of it.
# I guarantee nothing about this code, including but not limited to function or anything it
# may do to a computer you run it on.
# No checks whatsoever on security have been carried out.
# Be nice.

# This is written on Windows 8.1 and assumes that executable files are run under the
# Windows Command Processor (cmd)
# Python is Python 3.4.1, freely downloadable from http://python.org
# The ffmpeg version required must contain opengl support.

from string import Template
import argparse,  tempfile,  subprocess, json, pprint

def ffmpegEscape(input):
    return(input.replace("\\",  "\\\\").replace(":",  "\\:"))

## IMPORTANT -- CONFIGURATION ##
## PLEASE ENTER YOUR CONFIGURATION VALUES BELOW
##
##   The FULL PATH to your FFmpeg binary
##   Please keep the 'r' at the front

FFMPEG = r"c:/Program Files/ffmpeg/bin/"

##   The FULL PATHNAME of your font for the timecode

FONT = ffmpegEscape(r"c:/windows/fonts/arial.ttf")

##   The STARTING VALUE for your timecode

TIMECODE = ffmpegEscape("00:00:00:00")


########################################



# Write a file which becomes the LAVFI input to FFmpeg
# ...then write a DOS .bat file that calls FFmpeg with the LAVFI file as an argument
# ...then call the .bat file
# ...and return. Hopefully.




parser = argparse.ArgumentParser(description='Video and audio monitor. Requires 1 picture track and stereo audio.')
parser.add_argument('filename',  metavar='file',  help='video file to be displayed')

args =  parser.parse_args()
filename_raw = args.filename

# The filename might have backslashes and/or colons. These must be escaped for ffmpeg
filename = ffmpegEscape(filename_raw)


# We need to know how many frames-per-second are used
# FFprobe puts it in a JSON variable under 'stream', 'r_frame_rate'

dos_command=[FFMPEG+"ffprobe.exe", "-v", "quiet", "-hide_banner", "-print_format", "json", "-show_streams", "-select_streams", "v:0", filename]
ffprobeReturn = subprocess.check_output(dos_command, universal_newlines=True)
jReturn = json.loads(ffprobeReturn)
FPS= jReturn['streams'][0]['r_frame_rate']
CODEC= jReturn['streams'][0]['codec_long_name']
HEIGHT= jReturn['streams'][0]['height']
WIDTH= jReturn['streams'][0]['width']
FORMAT= jReturn['streams'][0]['pix_fmt']

print ("FPS: ", FPS)
print ("CODEC: ", CODEC)
print ("HEIGHT: ", HEIGHT, "WIDTH: ", WIDTH)
print ("FORMAT: ", FORMAT)




LAVFI = ("movie='$MOVIE':streams=dv+da [video][audio]; " +
            "[video]scale=512:-1, split=3[video1][video2][video3];" +
            "[audio]asplit=[audio1][audio2]; " +
            "[video1]waveform=mode=column:display=overlay:" +
            "mirror=1:components=7:envelope=instant:intensity=0.2, " +
            "drawgrid=x=-1:y=20:h=219:w=515:color=green,scale=w=512:h=512:flags=neighbor, " +
            "pad=w=812:h=812:color=gray [scopeout]; " +
            "[video2]scale=512:-1:flags=neighbor[monitorout]; " +
            "[audio1]ebur128=video=1:meter=18:framelog=verbose:peak=true[ebur128out][out1]; " +
            "[ebur128out]scale=300:300:flags=fast_bilinear[ebur128scaledout]; " +
            "[scopeout][ebur128scaledout]overlay=x=512:eval=init[videoandebu]; " +
            "[audio2]avectorscope=s=301x301:r=10:zoom=5, " +
            "drawgrid=x=149:y=149:t=2:color=green [vector]; " +
            "[videoandebu][monitorout]overlay=y=512:eval=init[comp3]; " +
            "[comp3][vector]overlay=x=512:y=300:eval=init, " +
            "setdar=1/1, setsar=1/1, " +
            "drawtext=fontfile='$FONT':timecode='$TIMECODE':" +
            "r=$FPS:x=726:y=0:fontcolor=white[comp]; " +
            "[video3]vectorscope=mode=color3, " +
            "scale=212:212[vectorout]; "+
            "[comp][vectorout]overlay=x=512:y=600:eval=init[out0]")
            


# Make up the string that the LAVFI file will contain

working = Template(LAVFI)
lavfi_string = working.substitute(MOVIE = filename,  FONT=FONT,  TIMECODE=TIMECODE, FPS=FPS)
# print ('LAVFI string is: ',  lavfi_string)


# Now create a named temporary file and write the LAVFI string to it.
# Prevent automatic deletion on closure
with tempfile.NamedTemporaryFile(delete=False) as lavfi_file:
    
    lavfi_filename = lavfi_file.name
    lavfi_file.write(lavfi_string.encode('utf-8'))
    lavfi_file.close()

print('Filename of temporary file is: ',  lavfi_filename)
dos_command = [FFMPEG+"ffplay.exe", "-threads", "auto", "-avioflags", "direct", "-seek2any", "1", "-err_detect", "aggressive", "-stats", "-fast", "-threads", "1", "-infbuf", "-f",  "lavfi", "-sws_flags", "neighbor", "-graph_file", lavfi_filename, "-i", ""]
# dos_command = [FFMPEG+"ffmpeg.exe", "-hwaccel", "dxva2", "-re", "-flags2", "fast", "-f",  "lavfi", "-graph_file", lavfi_filename, "-i", "", "-flags2", "fast", "-f", "opengl", "OUTPUT"]
subprocess.check_output(dos_command)












