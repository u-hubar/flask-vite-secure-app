from database.db import (
    Master,
    Service,
    User,
    db_session,
    FailedLoginLogs,
    UserLoginLogs,
)
from database.schemas import ServiceSchema, UserLoginLogsSchema
from flask import Flask, json, jsonify, request
from flask_script import Manager
from sqlalchemy.exc import IntegrityError

from backend.encryption.jwt_tokens import (
    decode_token,
    generate_token,
    token_required,
)
from backend.encryption.password import (
    decrypt_service_password,
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

    user_agent = request.headers.get("User-Agent", None)
    user_ip = request.remote_addr

    if user is None:
        email = data.get("email", None)
        password = data.get("password", None)
        failed_login = FailedLoginLogs(
            email=email,
            password=password,
            user_agent=user_agent,
            user_ip=user_ip,
        )
        db_session.add(failed_login)
        db_session.commit()
        return (
            jsonify({"status": "failed", "message": "Failed getting user"}),
            403,
        )

    user_login = UserLoginLogs(
        user_id=user.id, user_agent=user_agent, user_ip=user_ip
    )
    db_session.add(user_login)
    db_session.commit()

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

    if data[1] != 200:
        return data

    email = data[0]["sub"]
    access_token = generate_token(identity=email, seconds=15)

    return jsonify({"access": access_token})


@app.route("/api/master", methods=["GET", "POST"])
@token_required
def master_password(user_id):
    master_exists = Master.is_exists(user_id)

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
        data = request.get_json(force=True)
        master = data.get("master")

        if master_exists:
            master = Master.validate(user_id, master)

            if master is None:
                return (
                    jsonify(
                        {"status": "failed", "message": "Invalid master."}
                    ),
                    403,
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
            master = encrypt_user_password(master)
            new_master = Master(user_id=user_id, master=master)
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
def service(user_id):
    if request.method == "GET":
        service_schema = ServiceSchema(
            many=True, only=["id", "service", "url", "username"]
        )
        services = Service.query.filter_by(user_id=user_id).all()
        services_dump = service_schema.dump(services)

        return jsonify(services_dump), 200

    if request.method == "POST":
        data = request.get_json(force=True)
        service = data["service"]
        url = data["url"]
        username = data["username"]
        password = data["password"]

        master = Master.query.filter_by(user_id=user_id).first()
        master = master.master

        if master is None:
            return (
                jsonify({"status": "failed", "message": "Invalid master."}),
                403,
            )

        password = encrypt_service_password(
            master, password, service + username
        )

        new_service = Service(
            user_id=user_id,
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


@app.route("/api/passwords", methods=["POST"])
@token_required
def show_passwords(user_id):
    master = Master.query.filter_by(user_id=user_id).first()
    master = master.master

    if master is None:
        return (
            jsonify({"status": "failed", "message": "Invalid master."}),
            403,
        )

    passwords = Service.query.filter_by(user_id=user_id).all()

    if not passwords:
        return (
            jsonify({"status": "failed", "message": "No passwords."}),
            404,
        )

    passwords_dump = []
    for pswd in passwords:
        password = decrypt_service_password(
            master, pswd.password, pswd.service + pswd.username
        )
        passwords_dump.append({"id": pswd.id, "password": password})

    return jsonify(passwords_dump), 200


@app.route("/api/logs", methods=["GET"])
@token_required
def get_logs(user_id):
    logs_schema = UserLoginLogsSchema(many=True)
    logs = UserLoginLogs.query.filter_by(user_id=user_id).all()
    logs_dump = logs_schema.dump(logs)
    return jsonify(logs_dump), 200


if __name__ == "__main__":
    manager.run()
