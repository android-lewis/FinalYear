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

likes = Blueprint('likes', __name__, template_folder='route')

@likes.route("/")
def hello_world():
    return jsonify(hello="like")