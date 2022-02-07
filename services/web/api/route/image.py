from crypt import methods
from flask import (
    Blueprint,
    jsonify,
    request,
    current_app
)
from werkzeug.utils import secure_filename
from api.model.data_spec import Image
from api.helper.auth import token_required
import api.gan.infer as infer
from .. import db
from pathlib import Path

import uuid
import hashlib
import os

image = Blueprint('image', __name__)

@image.route("/")
def images():
    return jsonify(value=Image.query.all()), 200

@image.route("/get")
def getImage():
    if 'imageid' not in request.args:
        return jsonify(message="Please supply imageid"), 422
    
    return jsonify(message=f"Returing image with ID {request.args['imageid']}", value=Image.query.filter_by(image_id=request.args['imageid']).first()), 200

@image.route("/author")
def imagesByAuthor():
    if 'ownerid' not in request.args:
        return jsonify(message="Please supply ownerid"), 422
    
    return jsonify(value=Image.query.filter_by(owner_id=request.args['ownerid']).all()), 200

@image.route("/gallery")
def imagesByGallery():
    if 'galleryid' not in request.args:
        return jsonify(message="Please supply galleryid"), 422
    
    return jsonify(value=Image.query.filter_by(gallery_id=request.args['galleryid']).all()), 200

@image.route("/generate", methods=["POST"])
def generateImage(): 
    image_name = infer.generate()
    
    Path(f"api/images/generated/").mkdir(parents=True, exist_ok=True)
    file_location=f"/images/generated/{image_name}"
    
    return jsonify(message="Image Generated", value=file_location)

@image.route("/modify", methods=["PATCH"])
@token_required
def modifyImage(current_user):
    if not request.is_json:
        return jsonify(message="Missing JSON in request"), 400
    
    data = request.get_json()
    image_id = data["image_id"] if "image_id" in data else 0

    if image_id == 0:
        current_app.logger.debug(data)
        return jsonify(message="Please supply image_id"), 422
    
    # Get current image
    cur_image = Image.query.filter_by(image_id=image_id).first()
    current_app.logger.debug(f"Before update: {cur_image}")
    
    if not cur_image:
        return jsonify(message="image does not exist"), 404
    
    cur_image.gallery_id = data["gallery_id"] if "gallery_id" in data else cur_image.gallery_id
    cur_image.name = data["name"] if "name" in data else cur_image.name
    cur_image.description = data["description"] if "description" in data else cur_image.description
    
    current_app.logger.debug(f"After update: {cur_image}")
    current_app.logger.info(f"User {current_user.user_id} updated image with ID {cur_image.image_id}")
    
    db.session.commit()
    
    return jsonify(message=f"Returing image with ID {image_id}", value=cur_image), 200

@image.route("/upload", methods=["POST"])
def imageUpload():
    if 'file' not in request.files:
        return jsonify(message="Missing file data in request"), 400
    
    #dir_name = hashlib.md5(str(current_user.user_id).encode())
    #Path(f"api/images/uploaded/{dir_name.hexdigest()}").mkdir(parents=True, exist_ok=True)
    
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in current_app.config['UPLOAD_EXTENSIONS']:
            return jsonify(message="Image not accepted file type"), 400
        
        image_id = uuid.uuid4()
        
        new_file = f"/images/uploaded/{image_id}{file_ext}"
        uploaded_file.save(f"api/images/uploaded/{image_id}{file_ext}")
        #new_image = Image(image_id=image_id, owner_id=current_user.user_id, file_location=f"/images/uploaded/{dir_name.hexdigest()}/{image_id}{file_ext}", name=str(uuid.uuid4()))
    
    #current_app.logger.info(f"User {current_user.user_id} uploaded image with ID {new_image.image_id}")

    #db.session.add(new_image)
    #db.session.commit()

    return jsonify(message="Image Uploaded", value=new_file)

@image.route("/save", methods=["POST"])
@token_required
def saveImage(current_user):
    if 'file' not in request.files:
        return jsonify(message="Missing file data in request"), 400
    
    dir_name = hashlib.md5(str(current_user.user_id).encode())
    Path(f"api/images/combined/{dir_name.hexdigest()}").mkdir(parents=True, exist_ok=True)
    
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in current_app.config['UPLOAD_EXTENSIONS']:
            return jsonify(message="Image not accepted file type"), 400
        
        image_id = uuid.uuid4()
        
        uploaded_file.save(f"api/images/combined/{dir_name.hexdigest()}/{image_id}{file_ext}")
        new_image = Image(image_id=image_id, owner_id=current_user.user_id, file_location=f"/images/combined/{dir_name.hexdigest()}/{image_id}{file_ext}", name=str(uuid.uuid4()))
    
    current_app.logger.info(f"User {current_user.user_id} saved image with ID {new_image.image_id}")
    
    db.session.add(new_image)
    db.session.commit()

    return jsonify(message="Image Saved", value=new_image)

@image.route("/delete", methods=["DELETE"])
@token_required
def deleteImage(current_user):
    if 'imageid' not in request.args:
        return jsonify(message="Missing owner arg in request"), 400
    
    cur_img = Image.query.filter_by(image_id=request.args['imageid']).first()

    if not current_user.user_id == cur_img.owner_id:
        return jsonify(message="You must own this image to delete it")
    
    current_app.logger.info(f"User {current_user.user_id} deleted image with ID {cur_img.image_id}")

    db.session.delete(cur_img)
    db.session.commit()

    return jsonify(message="Image Deleted", value=cur_img)
        