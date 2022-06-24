from flask import Flask, request, make_response, jsonify
from flask_restful import Resource, Api
import jwt
import datetime

from functools import wraps

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = "syhrl"


#key
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        #parsing di parameter endpoint
        token = request.args.get('token')
        if not token:
            return make_response(jsonify({"msg":"Tidak ada Token"}), 404)

            #decode token yang diterima
        try:
            output = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return make_response(jsonify({"msg":"Token Tidak Valid"}))
        return f(*args, **kwargs)
    return decorator



# Endpoint Login
class LoginUser(Resource):
    def post(self):
        username = request.form.get('username')
        password = request.form.get('password')

        # Cek Password
        if username and password == 'user':
            # hasil nomor token
            token = jwt.encode(
                {
                    "username":username,
                    "exp":datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
                }, app.config['SECRET_KEY'], algorithm="HS256"
            )
            return jsonify({
                "token":token,
                "msg":"Berhasil Login Dan Masuk Laman"
            })

        return jsonify({"msg": "Silahkan Login Terlebih Dahulu"})

class Laman(Resource):
    @token_required
    def get(self):
        return jsonify({"msg":"Laman"})

class Home(Resource):
    def get(self):
        return jsonify({"msg":"Home"})


api.add_resource(LoginUser, "/login", methods=["POST"])
api.add_resource(Laman, "/laman", methods=["GET"])
api.add_resource(Home, "/home", methods=["GET"])

if __name__ == "__main__":
    app.run(debug=True)