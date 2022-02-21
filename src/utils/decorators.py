from flask import request, jsonify, make_response
from functools import wraps
from environs import Env
import json


env = Env()
env.read_env("src/config/.env")


def token_required(f):
    """
    a simple decorator that checks if the
    x-access-token header is present in the request
    and is equal to the predefined secret key.
    it is essential to the post http request in order
    to authenticate-ish the user.

    the -ish at the end of the authenticate is because
    this it not a secure way of authenticating the user.
    normally we would like to use a jwt token that is generated
    and decoded.
    """

    @wraps(f)
    def decorator(*args, **kwargs):

        token = None

        if 'X-Access-Token' in request.headers:
            token = request.headers['X-Access-Token']

        # if not token:
        #     return jsonify({'message': 'a valid token is missing'})

        if not token == env.str("SECRET_KEY"):
            response = make_response(json.dumps({'message': 'token is invalid'}), 403)

            return response

        return f(*args, **kwargs)
    return decorator