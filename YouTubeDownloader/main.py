import os

from flask import Flask, redirect, render_template, request
from pytube import Playlist, YouTube

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"


def create_app():
    return app


# Function to get the download path
def get_download_path(video_music):
    """Returns the default downloads path for linux or windows"""
    # Download path for windows
    if os.name == "nt":
        sub_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"
        downloads_guid = "{374DE290-123F-4565-9164-39C4925E467B}"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        return location
    # Download path for linux
    else:
        download_path = os.path.join(os.path.expanduser('~'))
        # Try to download the file in the given path
        try:
            folder_path = download_path + '/' + video_music + '/' + folder_name
            os.mkdir(folder_path)
        except FileExistsError:
            print("FOLDER ALREADY EXISTS")
        return folder_path


# Function to download video
def download_vid(url, answ_PS):
    install_here = get_download_path("Video")
    # Download a single video
    if answ_PS == "S":
        url.streams.get_by_itag(251).download(install_here)
    # Download a playlist of videos
    elif answ_PS == "P":
        for arq in url.videos:
            arq.streams.get_by_itag(251).first().download(install_here)


# Function to download audio
def download_aud(url, answ_PS):
    install_here = get_download_path("Music")
    # Download a single audio
    if answ_PS == "S":
        url.streams.get_by_itag(140).download(install_here)
    # Download a playlist of audios
    elif answ_PS == "P":
        for arq in url.videos:
            arq.streams.get_by_itag(140).download(install_here)


# Function to choose some options
def choose(url, answ_PS, answ_VA):
    # If the option is video
    if answ_VA == "V":
        download_vid(url, answ_PS)
    # If the option is audio
    elif answ_VA == "A":
        download_aud(url, answ_PS)


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        url = request.form.get("url")

        # Turn FOLDER_NAME into global to use in the function GET_DOWNLOAD_PATH
        global folder_name
        folder_name = request.form.get("foldername")

        answ_PS = request.form["choosePS"]
        answ_VA = request.form["chooseVA"]

        if not url:
            return render_template("error.html", message="No URL given")
        if not url.startswith("https://www.youtube.com/"):
            return render_template("error.html", message="Invalid URL")
        if not answ_PS:
            return render_template("error.html", message="File type not selected")
        if not answ_VA:
            return render_template("error.html", message="Invalid URL")

        # Call the function to choose between PLAYLIST OR SINGLE or VIDEO OR AUDIO
        if "submit_button" in request.form:
            choose(YouTube(url), answ_PS, answ_VA)
        return redirect("/")

    # Return the site base template
    else:
        return render_template("index.html")
