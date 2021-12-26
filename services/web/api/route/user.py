from flask import (
    Blueprint,
    jsonify,
    send_from_directory,
    request,
    redirect,
    url_for
)

from api.model.data_spec import User
from .. import db

import uuid

user = Blueprint('user', __name__, template_folder='route')

@user.route("/GetAllUsers")
def GetAllUsers():
    return jsonify(message="Serving all users", value=User.query.all())

@user.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify(token="none", message="Login failed")
    
    return jsonify(token=uuid.uuid4(), message="Login Success")

@user.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    fName = data['f_name']
    lName = data['l_name']
    email = data['email']
    password = data['password']

    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify(message="Please login")
    
    new_user = User(fName=fName, lName=lName, email=email)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify(token=uuid.uuid4(), message="User Registered", value=new_user)