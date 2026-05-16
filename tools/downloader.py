import os
import subprocess
from datetime import date
from utils.Downloader.lin import *
from utils.Downloader.win import *

def download_video(url, ext, playlist_name):
    sous_dossier = date.today().isoformat()
    
    chemin = os.path.join("output",sous_dossier)
    os.makedirs(chemin, exist_ok=True)

    if os.name == "nt":
        cmd = rf'.\utils\Downloader\win\yt-dlp.exe --restrict-filenames --ffmpeg-location ".\utils\Downloader\win\ffmpeg.exe" {ext} --embed-metadata --embed-thumbnail --convert-thumbnails jpg -o "{chemin}\{playlist_name}\%(uploader)s\%(title)s\%(title)s.%(ext)s" "{url}"'
        process = subprocess.Popen(cmd, shell=True)
        return process

    elif os.name == "posix":
        cmd = rf'./utils/Downloader/lin/yt-dlp_linux --restrict-filenames {ext} --embed-metadata --embed-thumbnail --convert-thumbnails jpg -o "{chemin}/{playlist_name}/%(uploader)s/%(title)s/%(title)s.%(ext)s" "{url}"'
        process = subprocess.Popen(cmd, shell=True)
        return process

#--ffmpeg-location "./utils/Downloader/lin/ffmpeg"