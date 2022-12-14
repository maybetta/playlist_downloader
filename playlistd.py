import yt_dlp
from numpy import loadtxt, c_
from numpy.random import rand
from re import sub
from os.path import exists
from os import makedirs, rename
from time import sleep
from conf import *


OUT_PATH = PL_PATH[:-4] + '/'
if not exists(OUT_PATH):
    makedirs(OUT_PATH)
print("Downloading playlist in %s" % OUT_PATH)


pl = loadtxt(PL_PATH, delimiter='\t', dtype='str', encoding='utf-8')
urls = list(pl[1:,3])
titles = pl[1:,0]
authors = pl[1:,1]
years = pl[1:,2]

illegal_chars= "[/<>:\"|?*\\\]"
authors = [sub(illegal_chars, "", a).strip() for a in authors]
titles = [sub(illegal_chars, "", t).strip() for t in titles]
years = [sub(illegal_chars, "", y).strip() for y in years]
filenames = [y + "-" + a + "-" + t + "." + FORMAT for (y, a, t) in c_[years, authors, titles]]

ids = []
for u in urls:
    start=u.find("?v=")+3
    end=u.find("&", start)
    if end == -1:
        ids.append(u[start:])
    else:
        ids.append(u[start:end])


unavailable = []
noid = []

ydl_opts = {
    'ffmpeg_location': FFMPEG_PATH,
    'paths': {'home': OUT_PATH},
    'outtmpl': {'default': "%(id)s.%(ext)s"},
    'format': 'm4a/bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': FORMAT,
    }],
}

for id, url, filename in c_[ids, urls, filenames]:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:

            outfile = OUT_PATH + filename
            dlfile = OUT_PATH + id + "." + FORMAT

            if exists(outfile):
                continue

            print('Attempting to download %s in temp file %s' % (url, dlfile))
            try:
                error_code = ydl.download(url)
            except PermissionError:
                # let file locks get released, then try again
                print('Downloaded file is locked, retrying')
                sleep(5)
                try:
                    error_code = ydl.download(url)
                except PermissionError:
                    print('Can\'t convert to requested format, leaving m4a unchanged')
                    dlfile = dlfile[:-len(FORMAT)] + ".temp.m4a"
                    outfile = outfile[:-len(FORMAT)] + ".m4a"

            if exists(dlfile):
                rename(dlfile, outfile)

                print('Saved as %s' % (outfile))
            else:
                print('Video has unrecognized id, leaving filename unchanged')
                noid.append(url)

            if PAUSE_DL:
                t = 10+50*rand()
                print('Waiting %.0fs' % t)
                sleep(t)

        except yt_dlp.utils.DownloadError:
            print('Video unavailable, skipping')
            unavailable.append([filename[:-len(FORMAT)], url])
            continue


if len(unavailable) > 0:
    print('\nThese videos are unavailable:')
    for fn, url in unavailable:
        print(fn + " " + url)

if len(noid) > 0:
    print('\nThese videos have weird links:')
    for url in noid:
        print(url)
