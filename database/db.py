from backend.encryption.password import verify_user_password
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship, scoped_session, sessionmaker

engine = create_engine('sqlite:///database/database.sqlite', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, nullable=False, primary_key=True)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(256), nullable=False)
    master = relationship("Master", backref=backref("user", uselist=False))
    services = relationship('Service', backref="user", lazy=False)

    def __init__(self, email=None, password=None):
        self.email = email
        self.password = password

    def __repr__(self):
        return f'<User {self.email}>'

    @classmethod
    def authenticate(cls, **kwargs):
        email = kwargs.get('email')
        password = kwargs.get('password')

        if not email or not password:
            return None

        user = cls.query.filter_by(email=email).first()
        if not user or not verify_user_password(user.password, password):
            return None

        return user


class Master(Base):
    __tablename__ = 'masters'

    id = Column(Integer, nullable=False, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    master = Column(String(256), nullable=False)

    @classmethod
    def is_exists(cls, **kwargs):
        user_id = kwargs.get('user_id')

        if not user_id:
            return None

        master = cls.query.filter_by(user_id=user_id).first()
        if not master:
            return False

        return True

    @classmethod
    def validate(cls, **kwargs):
        user_id = kwargs.get('user_id')
        user_master = kwargs.get('master')

        if not user_id:
            return None

        master = cls.query.filter_by(user_id=user_id).first()
        if not master or not verify_user_password(master.master, user_master):
            return None

        return user_master


class Service(Base):
    __tablename__ = 'services'

    id = Column(Integer, nullable=False, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    service = Column(String(50), nullable=False)
    url = Column(String(128), nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(256), nullable=False)


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
