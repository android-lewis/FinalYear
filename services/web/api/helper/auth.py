from flask import request, jsonify, current_app
import jwt
from functools import wraps
from api.model.data_spec import User

def token_required(f):
  @wraps(f)
  def decorator(*args, **kwargs):
    token = None

    if 'x-access-tokens' in request.headers:
      token = request.headers['x-access-tokens']

    if not token:
      return jsonify(message="A valid token is missing")
    
    try:
      data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms="HS256")
      cur_user = User.query.filter_by(user_id=data['user_id']).first()
    except:
      return jsonify(message="Invalid token, please login")
    
    return f(cur_user, *args, **kwargs)
  return decorator