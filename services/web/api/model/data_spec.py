from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from sqlalchemy.dialects.postgresql import UUID
import uuid
from .. import db

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