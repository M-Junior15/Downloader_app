import os
import jinja2
import instaloader
from flask import Flask, redirect, render_template, request
from pytube import Playlist, YouTube


app = Flask(__name__, template_folder="templates")

jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader("templates"))


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
        download_path = os.path.join(os.path.expanduser("~"))
        # Try to download the file in the given path
        try:
            folder_path = download_path + "/" + video_music + "/" + folder_name
            os.mkdir(folder_path)
        # If file already exist
        except FileExistsError:
            print("FOLDER ALREADY EXISTS")
        return folder_path


# Function to download video
def download_yt_vid(url, answ_PS):
    install_here = get_download_path("Videos")
    # Download a single video
    if answ_PS == "S":
        print(url.streams)
        url.streams.get_by_itag(22).download(install_here)
    # Download a playlist of videos
    elif answ_PS == "P":
        for arq in url.videos:
            arq.streams.get_by_itag(22).first().download(install_here)


# Function to download audio
def download_yt_aud(url, answ_PS):
    install_here = get_download_path("Music")
    # Download a single audio
    if answ_PS == "S":
        url.streams.get_by_itag(140).download(install_here)
    # Download a playlist of audios
    elif answ_PS == "P":
        for arq in url.videos:
            arq.streams.get_by_itag(140).download(install_here)


# Function to choose some options
def choose_yt(url, answ_PS, answ_VA):
    # If the option is video
    if answ_VA == "V":
        download_yt_vid(url, answ_PS)
    # If the option is audio
    elif answ_VA == "A":
        download_yt_aud(url, answ_PS)


@app.route("/", methods=["POST", "GET"])
def yout_func():
    if request.method == "POST":
        # Errors
        if not request.form.get("url"):
            return render_template("error.html")
        if not request.form.get("foldername"):
            return render_template("error.html")
        if not request.form.get("choosePV"):
            return render_template("error.html")

        url = request.form.get("url")

        # Turn FOLDER_NAME into global to use in the function GET_DOWNLOAD_PATH
        global folder_name
        folder_name = request.form.get("foldername")

        answ_PS = request.form["choosePS"]
        answ_VA = request.form["chooseVA"]

        # Call the function to choose between PLAYLIST, SINGLE, VIDEO or AUDIO
        if "submit_button" in request.form:
            choose_yt(YouTube(url), answ_PS, answ_VA)
        return redirect("/")

    # Return the site base template
    else:
        return render_template("yout.html")


# Function to choose POST or VIDEO
def choose_it(url, answ_PV):
    # Instance of instaloader
    instance = instaloader.Instaloader()

    post = instaloader.Post.from_shortcode(
        instance.context, url.split("p/")[1].strip("/ ")
    )

    # If the option is PHOTO
    if answ_PV == "P":
        install_here = get_download_path("Pictures")
        instance.download_post(post, "")
    # If the option is VIDEO
    elif answ_PV == "V":
        install_here = get_download_path("Videos")
        instance.download_post(post, "")


@app.route("/insta", methods=["POST", "GET"])
def insta_func():
    if request.method == "POST":
        # Errors
        if not request.form.get("url"):
            return render_template("error.html")
        if not request.form.get("foldername"):
            return render_template("error.html")
        if not request.form.get("choosePV"):
            return render_template("error.html")

        # Get post URL from insta.html file
        url = request.form.get("url")

        global folder_name
        folder_name = request.form.get("foldername")

        answ_PV = request.form["choosePV"]

        # Call the function to choose between PHOTO or VIDEO
        if "submit_button" in request.form:
            choose_it(url, answ_PV)
        return redirect("/")
    else:
        return render_template("insta.html")

