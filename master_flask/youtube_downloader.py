from __future__ import unicode_literals
import youtube_dl
import sys
from video_segmenter import video_splitter

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d["status"] == "finished":
        print("Done downloading ...")


ydl_opts = {
    "format": None,
    "logger": MyLogger(),
    "outtmpl": "",
    "progress_hooks": [my_hook],
}


def download_video(url, location=""):
    tmp = "%(title)s.%(ext)s"
    ydl_opts["outtmpl"] = location + tmp
    info = None
    title = None
    ext = None
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        #ydl.download([url])
        info = ydl.extract_info(url, download=True)
        title = info.get('title', None)
        ext = info.get('ext', None)
    filename = title + '.' + ext
    return filename


def main(argv):
    if len(argv) != 1:
        print("Please only provide one argument: a youtube video url")
        return
    download_video(argv[0])


if __name__ == "__main__":
    main(sys.argv[1:])
