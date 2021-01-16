from database.db import Master, Service, User, db_session
from database.schemas import ServiceSchema
from flask import Flask, jsonify, request
from flask_script import Manager
from sqlalchemy.exc import IntegrityError

from backend.encryption.jwt_tokens import (
    decode_token,
    generate_token,
    token_required,
)
from backend.encryption.password import (
    encrypt_user_password,
    encrypt_service_password,
)

app = Flask(__name__)

manager = Manager(app)


@manager.command
def run():
    app.run()


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = encrypt_user_password(data.get("password"))

    try:
        new_user = User(email=email, password=password)
        db_session.add(new_user)
        db_session.commit()
    except IntegrityError as e:
        db_session.rollback()
        error = str(e).split("\n")[0]
        return (
            jsonify(
                {
                    "status": "failed",
                    "message": "Could not add user",
                    "error": f"{error}",
                }
            ),
            400,
        )

    return (
        jsonify({"status": "success", "message": "User added successfuly"}),
        201,
    )


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.authenticate(**data)

    if user is None:
        return (
            jsonify({"status": "failed", "message": "Failed getting user"}),
            401,
        )

    access_token = generate_token(identity=user.email, seconds=15)
    refresh_token = generate_token(identity=user.email, seconds=86400)  # 24h

    return (
        jsonify(
            {
                "access": access_token,
                "refresh": refresh_token,
            }
        ),
        200,
    )


@app.route("/api/token_refresh", methods=["POST"])
def refresh():
    data = request.get_json()
    refresh_token = data.get("refresh", None)

    if refresh_token is None:
        return jsonify({"status": "failed", "message": "Invalid token."}), 401

    data = decode_token(refresh_token)

    if not data.get("authenticated"):
        return data

    email = data.get("email")
    access_token = generate_token(identity=email, seconds=15)

    return jsonify({"access": access_token})


@app.route("/api/master", methods=["GET", "POST"])
@token_required
def master_password(current_user):
    master_exists = Master.is_exists(user_id=current_user.id)

    if master_exists is None:
        return jsonify({"status": "failed", "message": "Invalid user."}), 401

    if request.method == "GET":
        if master_exists:
            return (
                jsonify({"status": "success", "message": "Master exists"}),
                200,
            )
        else:
            return (
                jsonify(
                    {"status": "failed", "message": "Master doesn't exist"}
                ),
                400,
            )

    if request.method == "POST":
        data = request.get_json()
        master = encrypt_user_password(data.get("master"))

        if master_exists:
            master = Master.validate(user=current_user, master=master)

            if master is None:
                return (
                    jsonify(
                        {"status": "failed", "message": "Invalid master."}
                    ),
                    401,
                )

            return (
                jsonify(
                    {
                        "status": "success",
                        "message": "Master password successfuly verified",
                    }
                ),
                200,
            )
        else:
            new_master = Master(user=current_user, master=master)
            db_session.add(new_master)
            db_session.commit()

            return (
                jsonify(
                    {
                        "status": "success",
                        "message": "Master password added successfuly",
                    }
                ),
                201,
            )


@app.route("/api/service", methods=["GET", "POST"])
@token_required
def service(current_user):
    if request.method == "GET":
        service_schema = ServiceSchema(
            many=True, only=["service", "url", "username"]
        )
        services = Service.query.filter_by(user_id=current_user.id).all()
        services_dump = service_schema.dump(services)

        return services_dump, 200

    if request.method == "POST":
        data = request.get_json()
        service = data["service"]
        url = data["url"]
        username = data["username"]
        password = data["password"]

        master = encrypt_user_password(data.get("master"))
        master = Master.validate(user=current_user, master=master)

        if master is None:
            return (
                jsonify({"status": "failed", "message": "Invalid master."}),
                401,
            )

        password = encrypt_service_password(
            master, password, service + username
        )

        new_service = Service(
            user=current_user,
            service=service,
            url=url,
            username=username,
            password=password,
        )
        db_session.add(new_service)
        db_session.commit()

        return (
            jsonify(
                {"status": "success", "message": "Service added successfuly"}
            ),
            201,
        )


@app.route('/api/passwords', methods=["POST"])
@token_required
def show_passwords(current_user):
    data = request.get_json()

    master = encrypt_user_password(data.get("master"))
    master = Master.validate(user=current_user, master=master)

    if master is None:
        return (
            jsonify({"status": "failed", "message": "Invalid master."}),
            401,
        )

    service_schema = ServiceSchema(
        many=True, only=["password"]
    )
    passwords = Service.query.filter_by(user_id=current_user.id).all()
    passwords_dump = service_schema.dump(passwords)

    return passwords_dump, 200


if __name__ == "__main__":
    manager.run()
