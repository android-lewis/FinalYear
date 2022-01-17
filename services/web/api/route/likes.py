from flask import (
    Flask,
    Blueprint,
    jsonify,
    send_from_directory,
    request,
    redirect,
    url_for
)

from api.model.data_spec import LikedImage
from .. import db

import os

from api.model.data_spec import LikedImage

likes = Blueprint('likes', __name__, template_folder='route')

@likes.route("/")
def likesByImage():
    if 'imageid' not in request.args:
        return jsonify(message="Missing image arg in request"), 400
    return jsonify(message=f"Returning likes for image {id}", value=LikedImage.Query.filter_by(image_id=request.args["image_id"]).all())

@likes.route("/like")
def switchLike():
    if ['imageid', 'owner_id'] not in request.args:
        return jsonify(message="Please include owner and image arg in request"), 400
    
    cur_like = LikedImage.Query.filter_by(owner_id=request.args["owner_id"], image_id=request.args["image_id"])

    if not cur_like:
        new_like = LikedImage(request.args["owner_id"], request.args["image_id"])
        db.session.add(new_like)
    else:
        db.session.delete(cur_like)  
    
    db.session.commit()