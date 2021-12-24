from werkzeug.utils import secure_filename
from flask import (
    Flask,
    Blueprint,
    jsonify,
    send_from_directory,
    request,
    redirect,
    url_for
)

import os

test_page = Blueprint('test_page', __name__, template_folder='route')

@test_page.route("/")
def hello_world():
    return jsonify(hello="world")

@test_page.route("/static/<path:filename>")
def staticfiles(filename):
    return send_from_directory(test_page.config["STATIC_FOLDER"], filename)

@test_page.route("/images/<path:filename>")
def imagefiles(filename):
    return send_from_directory(test_page.config["MEDIA_FOLDER"], filename)

@test_page.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        filename = secure_filename(file.filename)
        file.save(os.path.join(test_page.config["MEDIA_FOLDER"], filename))
    return """
    <!doctype html>
    <title>upload new File</title>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file><input type=submit value=Upload>
    </form>
    """