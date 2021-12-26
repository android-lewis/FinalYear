from flask import (
    Blueprint,
    jsonify,
    send_from_directory,
    request,
    redirect,
    url_for
)
from api.model.data_spec import Image
from .. import db

import os
import uuid

image = Blueprint('image', __name__, template_folder='route')

@image.route("/GetAllImages")
def images():
    return jsonify(value=Image.query.all())

@image.route("/GenerateImage", methods=["POST"])
def generateImage():
    data = request.get_json()
    owner_id = data['owner_id']

    new_image = Image(owner_id=owner_id, file_location="/static/test.png", name=str(uuid.uuid4()))

    db.session.add(new_image)
    db.session.commit()

    return jsonify(message="Image Created", value=Image.query.all())