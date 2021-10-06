from flask import Flask, jsonify, request, make_response
import jwt 
import datetime
from functools import wraps

app = Flask(__name__)

app.config['PRIVATE KEY'] = 'chrischrischris'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token') 

        if not token:
            return jsonify({'message' : 'AUTH TOKEN MISSING'}), 401

        try: 
            data = jwt.decode(token, app.config['PRIVATE KEY'])
        except:
            return jsonify({'message' : 'Token is invalid'}), 401

        return f(*args, **kwargs)

    return decorated

@app.route('/getCar')
def getCar():
    return jsonify({'message' : 'Welcome to the car shop'})

@app.route('/buyCar')
@token_required
def buyCar():
    return jsonify({'message' : 'You are now logged in'})

@app.route('/login')
def login():
    auth = request.authorization

    if auth and auth.password == '123':
        token = jwt.encode({'user' : auth.username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(hours=24)}, app.config['PRIVATE KEY'])

        return jsonify({'token' : token.decode('UTF-8')})

    return make_response('Log in error', 401, {'WWW-Authenticate' : 'Basic realm="Please Login"'})

if __name__ == '__main__':
    app.run(debug=True)
