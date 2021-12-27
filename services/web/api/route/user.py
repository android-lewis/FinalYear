from flask import (
    Blueprint,
    jsonify,
    send_from_directory,
    request,
    redirect,
    url_for,
    current_app
)

from api.model.data_spec import User
from .. import db

import uuid

user = Blueprint('user', __name__, template_folder='route')

@user.route("/GetAllUsers")
def GetAllUsers():
    return jsonify(message="Serving all users", value=User.query.all()), 200

@user.route("/GetUser", methods=["POST"])
def GetUser():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    
    data = request.get_json()
    user_id = data['user_id']
    current_app.logger.debug(data)
    return jsonify(message=f"Returing user with ID {user_id}", value=User.query.filter_by(user_id=user_id).first()), 200

@user.route("/ModifyUser", methods=["POST"])
def ModifyUser():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    
    data = request.get_json()
    user_id = data["user_id"] if "user_id" in data else 0

    if user_id == 0:
        current_app.logger.debug(data)
        return jsonify(message="Please supply user_id"), 422
    
    # Get current user
    cur_user = User.query.filter_by(user_id=user_id).first()
    current_app.logger.debug(f"Before update: {cur_user}")
    
    if not cur_user:
        return jsonify(message="User does not exist"), 404
    
    cur_user.fName = data["f_name"] if "f_name" in data else cur_user.fName
    cur_user.lName = data["l_name"] if "l_name" in data else cur_user.lName
    cur_user.bio = data["bio"] if "bio" in data else cur_user.bio
    cur_user.profile_image = data["profile_image"] if "profile_image" in data else cur_user.profile_image
    
    current_app.logger.debug(f"After update: {cur_user}")
    
    return jsonify(message=f"Returing user with ID {user_id}", value=User.query.filter_by(user_id=user_id).first()), 200

@user.route("/login", methods=["POST"])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    
    data = request.get_json()
    email = data['email']
    password = data['password']
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify(token="none", message="Login failed"), 401
    
    return jsonify(token=uuid.uuid4(), message="Login Success"), 200

@user.route("/register", methods=["POST"])
def register():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    
    data = request.get_json()

    fName = data['f_name']
    lName = data['l_name']
    email = data['email']
    password = data['password']

    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify(message="User already exists, please login"), 409
    
    new_user = User(fName=fName, lName=lName, email=email)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify(token=uuid.uuid4(), message="User Registered", value=new_user), 200