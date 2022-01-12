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

gallery = Blueprint('gallery', __name__, template_folder='route')

@gallery.route("/")
def hello_world():
    return jsonify(hello="gallery")