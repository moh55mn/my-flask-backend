from flask import Flask, request, jsonify
from flask_cors import CORS
from backend.models import db, User
import os

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABSE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()
    if User.query.count() == 0:
        user = User(username="admin", password="1234")
        db.sesssion.add(user)
        db.session.commit()

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username, password=password).first()
    if user:
        return jsonify({"sucess": True, "message": "login succiful"})
    else:
        return jsonify({"sucess": False, "message": "invalid logins"}), 401

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


