from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from flask import (
    Flask,
    jsonify,
    send_from_directory,
    request,
    redirect,
    url_for
)

import os
import uuid

app = Flask(__name__)
app.config.from_object("src.config.Config")
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    fName = db.Column(db.String(32), index=True)
    lName = db.Column(db.String(32), index=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    bio = db.Column(db.String(255))
    profile_image = db.Column(db.String(128))
    images = db.relationship('Image', backref="owned_images", lazy=True)
    galleries = db.relationship('Gallery', backref="owned_galleries", lazy=True)
    likes = db.relationship('LikedImage', backref="liked_images", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, email):
        self.email = email

class Image(db.Model):
    __tablename__ = "image"

    image_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    gallery_id = db.Column(UUID(as_uuid=True), db.ForeignKey('gallery.gallery_id'))
    file_location = db.Column(db.String(128), nullable=False)
    created = db.Column(db.DateTime(), nullable=False)
    name = db.Column(db.String(32), index=True)
    description = db.Column(db.String(255))
    likes = db.relationship('LikedImage', backref="likes_on_image", lazy=True)

class Gallery(db.Model):
    __tablename__ = "gallery"

    gallery_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    name = db.Column(db.String(32), index=True)
    description = db.Column(db.String(255))
    visibility = db.Column(db.Boolean(), default=True, nullable=False)
    images = db.relationship('Image', backref="images_in_gallery", lazy=True)

class LikedImage(db.Model):
    __tablename__ = "liked_image"

    like_id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    image_id = db.Column(UUID(as_uuid=True), db.ForeignKey('image.image_id'))

@app.route("/")
def hello_world():
    return jsonify(hello="world")

@app.route("/static/<path:filename>")
def staticfiles(filename):
    return send_from_directory(app.config["STATIC_FOLDER"], filename)

@app.route("/images/<path:filename>")
def imagefiles(filename):
    return send_from_directory(app.config["MEDIA_FOLDER"], filename)

@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["MEDIA_FOLDER"], filename))
    return """
    <!doctype html>
    <title>upload new File</title>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file><input type=submit value=Upload>
    </form>
    """