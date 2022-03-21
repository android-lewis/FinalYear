from flask import (
    Blueprint,
    jsonify,
    request,
    current_app
)

from flask_mail import Message
from api.model.data_spec import User
from api.helper.auth import token_required
from .. import db, mail

import jwt
import uuid
import datetime

user = Blueprint('user', __name__)

@user.route("/")
def GetAllUsers():
    return jsonify(message="Serving all users", value=User.query.all()), 200

@user.route("/get")
@token_required
def GetUser(current_user):
    return jsonify(message=f"Returing user with ID {current_user.user_id}", value=User.query.filter_by(user_id=current_user.user_id).first()), 200

@user.route("/modify", methods=["POST"])
def ModifyUser():
    if not request.is_json:
        return jsonify(message="Missing JSON in request"), 400
    
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
        current_app.logger.debug("Missing JSON in request")
        return jsonify(message="Missing JSON in request"), 400
    
    data = request.get_json()
    keys = ['email', 'password']
    """
    msg = Message(
        'Hello',
        sender='abstract.styler@gmail.com',
        recipients = ['lewisbaston2@gmail.com']
    )
    
    msg.body = 'Test from Flask'
    mail.send(msg)
    
    """
    if not all(key in data for key in keys):
        current_app.logger.debug("Please supply all required fields")
        return jsonify(message="Please supply all required fields"), 422
    
    email = data['email']
    password = data['password']
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        current_app.logger.debug("Login failed")
        return jsonify(token="none", message="Login failed"), 401
    
    token = jwt.encode({'user_id': user.user_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, current_app.config['SECRET_KEY'], algorithm="HS256")
    return jsonify(token=token, message="Login Success"), 200

@user.route("/register", methods=["POST"])
def register():
    if not request.is_json:
        current_app.logger.debug("Missing JSON in request")
        return jsonify(message="Missing JSON in request"), 400
    
    data = request.get_json()
    keys = ['f_name', 'l_name', 'email', 'password']

    if not all(key in data for key in keys):
        current_app.logger.debug("Please supply all required fields")
        return jsonify(message="Please supply all required fields"), 422
    
    fName = data['f_name']
    lName = data['l_name']
    email = data['email']
    password = data['password']

    user = User.query.filter_by(email=email).first()
    if user:
        current_app.logger.debug("User already exists, please login")
        return jsonify(message="User already exists, please login"), 409
    
    new_user = User(fName=fName, lName=lName, email=email)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify(message="User Registered", value=new_user), 200