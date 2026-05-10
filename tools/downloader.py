import os
import subprocess
from datetime import date
from utils.Downloader.lin import *
from utils.Downloader.win import *

def download_video(url):
    sous_dossier = date.today().isoformat()
    
    chemin = os.path.join("output",sous_dossier)
    os.makedirs(chemin, exist_ok=True)

    if os.name == "nt":
        cmd = rf'.\utils\Downloader\win\yt-dlp.exe --ffmpeg-location ".\utils\Downloader\win\ffmpeg.exe" -x --audio-format mp3 --audio-quality 0 --embed-metadata --embed-thumbnail --convert-thumbnails jpg -o "{chemin}\%(uploader)s\%(title)s\%(title)s" "{url}"'
        process = subprocess.Popen(cmd, shell=True)
        return process

    elif os.name == "posix":
        cmd = rf'.\utils\Downloader\lin\yt-dlp --ffmpeg-location ".\utils\Downloader\lin\ffmpeg" -x --audio-format mp3 --audio-quality 0 --embed-metadata --embed-thumbnail --convert-thumbnails jpg -o "{chemin}\%(uploader)s\%(title)s\%(title)s" "{url}"'
        process = subprocess.Popen(cmd, shell=True)
        return process

