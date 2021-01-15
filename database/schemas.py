from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from database.db import User, Master, Service


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
