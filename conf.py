from os.path import expanduser
HOME = expanduser("~").replace('\\','/')


# path to playlist. Download from google sheets as "Tab separated values"
PL_PATH = HOME + '/Desktop/music/80s (and really good 1970s) Playlist 4 Maybetta - Sheet1.tsv'

# needs FFMPEG, preferably from https://github.com/yt-dlp/FFmpeg-Builds#ffmpeg-static-auto-builds
FFMPEG_PATH = 'C:/Program Files/ffmpeg-ytdlp/bin/'

# pauses for 10-60s after every download
PAUSE_DL = True

# mp3, m4a, flac, vorbis, aac, alac, opus, wav
FORMAT = "mp3"
