from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from database.db import User, Master, Service, UserLoginLogs, FailedLoginLogs


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True


class MasterSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Master
        include_fk = True
        load_instance = True


class ServiceSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Service
        include_fk = True
        load_instance = True


class UserLoginLogsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UserLoginLogs
        include_fk = True
        load_instance = True


class FailedLoginLogsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = FailedLoginLogs
        include_fk = True
        load_instance = True
