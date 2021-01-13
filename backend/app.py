from flask import Flask, jsonify, request
from flask_script import Manager
from backend.hashing.encryption import encrypt_user_password


from database.db import db_session, User

app = Flask(__name__)

manager = Manager(app)

@manager.command
def run():
    app.run()


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/api/register', methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = encrypt_user_password(data.get("password"))

    try:
        new_user = User(username=username, password=password)
        db_session.add(new_user)
        db_session.commit()
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Could not add user",
            "error": f"{e}"
        })

    return jsonify({
        "status": "success",
        "message": "User added successfully"
    }), 201


if __name__ == "__main__":
    manager.run()
