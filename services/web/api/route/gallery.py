from flask import (
    Blueprint,
    jsonify,
    request,
    current_app
)
from api.model.data_spec import Gallery
from api.helper.auth import token_required
from .. import db

gallery = Blueprint('gallery', __name__, template_folder='route')

@gallery.route("/")
def getAllGalleries():
    return jsonify(value=Gallery.query.all()), 200

@gallery.route("/get")
def getGallery():
    if 'galleryid' not in request.args:
        return jsonify(message="Please supply galleryid"), 422
    
    return jsonify(message=f"Returing gallery with ID {request.args['galleryid']}", value=Gallery.query.filter_by(gallery_id=request.args['galleryid']).first()), 200

@gallery.route("/user")
def getUserGalleries():    
    if 'ownerid' not in request.args:
        return jsonify(message="Please supply ownerid"), 422
    
    return jsonify(message=f"Returing galleries belonging to user with ID {request.args['ownerid']}", value=Gallery.query.filter_by(owner_id=request.args['ownerid']).all()), 200

@gallery.route("/create", methods=["POST"])
@token_required
def createGallery(current_user):
    if not request.is_json:
        return jsonify(message="Missing JSON in request"), 400
    
    data = request.get_json()
    keys = ['name', 'visibility']

    if not all(key in data for key in keys):
        return jsonify(message="Please supply all required fields"), 422

    owner_id = current_user.owner_id
    name = data['name']
    visibility = data['visibility']
    
    new_gal = Gallery(owner_id, name, visibility)
    
    db.session.add(new_gal)
    db.session.commit()

    return jsonify(message="Gallery created", value=new_gal), 200

@gallery.route("/modify", methods=["PATCH"])
@token_required
def modifyGallery(current_user):
    if not request.is_json:
        return jsonify(message="Missing JSON in request"), 400
    
    data = request.get_json()
    gallery_id = data["gallery_id"] if "gallery_id" in data else 0

    if gallery_id == 0:
        current_app.logger.debug(data)
        return jsonify(message="Please supply gallery_id"), 422
    
    # Get current image
    cur_gal = Gallery.query.filter_by(gallery_id=gallery_id).first()
    current_app.logger.debug(f"Before update: {cur_gal}")
    
    if not cur_gal:
        return jsonify(message="Gallery does not exist"), 404

    if cur_gal.owner_id == current_user.user_id:
        cur_gal.name = data['name'] if "name" in data else cur_gal.name
        cur_gal.description = data['desc'] if "desc" in data else cur_gal.description
        cur_gal.visibility = data['visibility'] if "visibility" in data else cur_gal.visibility
        cur_gal.thumbnail = data['thumbnail'] if "thumbnail" in data else cur_gal.thumbnail
        
        db.session.commit()

        return jsonify(message="Gallery created", value=cur_gal), 200
    
    return jsonify(message="You do not own this gallery"), 401

@gallery.route("/delete", methods=["DELETE"])
@token_required
def deleteGallery(current_user):
    if 'galleryid' not in request.args:
        return jsonify(message="Missing owner arg in request"), 400
    
    cur_gal = Gallery.query.filter_by(gallery_id=request.args['galleryid']).first()
    
    if cur_gal.owner_id == current_user.user_id:
        db.session.delete(cur_gal)
        db.session.commit()

        return jsonify(message="Image Deleted", value=cur_gal)
    
    return jsonify(message="You do not own this gallery"), 401