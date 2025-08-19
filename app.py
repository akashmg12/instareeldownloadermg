from flask import Flask, request, send_file, render_template, redirect, url_for
import yt_dlp
import os

app = Flask(__name__)

# File path for downloaded video
OUTPUT_FILE = "static/downloaded_video.mp4"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]

        # yt-dlp options
        ydl_opts = {
            "outtmpl": OUTPUT_FILE,
            "format": "mp4"
        }

        # Download video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Redirect to options page
        return redirect(url_for("options"))

    return render_template("index.html")


@app.route("/options")
def options():
    return render_template("options.html", video_file=OUTPUT_FILE)


@app.route("/view")
def view_video():
    return f"""
    <video width="720" controls autoplay>
        <source src='/{OUTPUT_FILE}' type='video/mp4'>
        Your browser does not support HTML5 video.
    </video>
    <br>
    <a href='/options'>⬅ Back</a>
    """


@app.route("/download")
def download_video():
    return send_file(OUTPUT_FILE, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
