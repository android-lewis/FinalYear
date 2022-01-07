from flask import (
    Blueprint,
    jsonify,
    request,
    current_app
)
from werkzeug.utils import secure_filename
from api.model.data_spec import Image
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
    if not request.is_json:
        return jsonify(message="Missing JSON in request"), 400
    
    data = request.get_json()
    if 'image_id' not in data:
        return jsonify(message="Please supply image_id"), 422
    
    current_app.logger.debug(data)
    return jsonify(message=f"Returing user with ID {data['image_id']}", value=Image.query.filter_by(image_id=data['image_id']).first()), 200

@image.route("/author", methods=["POST"])
def imagesByAuthor():
    data = request.get_json()
    if 'owner_id' not in data:
        return jsonify(message="Please supply owner_id"), 422
    
    return jsonify(value=Image.query.filter_by(owner_id=data['owner_id'])), 200

@image.route("/gallery", methods=["POST"])
def imagesByGallery():
    data = request.get_json()
    if 'gallery_id' not in data:
        return jsonify(message="Please supply gallery_id"), 422
    
    return jsonify(value=Image.query.filter_by(gallery_id=data['gallery_id'])), 200

@image.route("/generate", methods=["POST"])
def generateImage():
    data = request.get_json()
    owner_id = data['owner_id'] if 'owner_id' in data else 0
    
    if owner_id == 0:
        current_app.logger.debug(data)
        return jsonify(message="Please supply owner_id"), 422
    
    dir_name = hashlib.md5(str(owner_id).encode())
    Path(f"api/images/{dir_name.hexdigest()}").mkdir(parents=True, exist_ok=True)
    current_app.logger.debug(data)
    image_id = uuid.uuid4()
    new_image = Image(image_id=image_id, owner_id=owner_id, file_location=f"/images/{dir_name.hexdigest()}/{image_id}.png", name=str(uuid.uuid4()))

    db.session.add(new_image)
    db.session.commit()

    return jsonify(message="Image Created", value=new_image)

@image.route("/modify", methods=["POST"])
def modifyImage():
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
    
    return jsonify(message=f"Returing image with ID {image_id}", value=Image.query.filter_by(image_id=image_id).first()), 200

@image.route("/upload", methods=["POST"])
def imageUpload():
    if 'file' not in request.files:
        return jsonify(message="Missing file data in request"), 400
    if 'owner' not in request.args:
        return jsonify(message="Missing owner arg in request"), 400
    
    dir_name = hashlib.md5(str(request.args['owner']).encode())
    Path(f"api/images/{dir_name.hexdigest()}").mkdir(parents=True, exist_ok=True)
    
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in current_app.config['UPLOAD_EXTENSIONS']:
            return jsonify(message="Image not accepted file type"), 400
        
        image_id = uuid.uuid4()
        
        uploaded_file.save(f"api/images/{dir_name.hexdigest()}/{image_id}{file_ext}")
        new_image = Image(image_id=image_id, owner_id=request.args['owner'], file_location=f"/images/{dir_name.hexdigest()}/{image_id}{file_ext}", name=str(uuid.uuid4()))
    
    db.session.add(new_image)
    db.session.commit()

    return jsonify(message="Image Uploaded", value=new_image)
        