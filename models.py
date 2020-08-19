from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    full_name = db.Column(db.Text, nullable=False)

    @classmethod
    def signup(cls, email, username, password, full_name):
        """sign up and hash password"""
        hashed_pw = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(email=email, username=username, password=hashed_pw, full_name=full_name)
        db.session.add(user)

        return user
    
    @classmethod
    def login(cls, username, password):
        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

class Favorite(db.Model):
    __tablename__ = "favorites"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'), nullable=False)
    recipes = db.Column(db.Integer, nullable=False)
    name = db.Column(db.Text, nullable=False)

    user = db.relationship('User', backref='favorites')

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "recipes": self.recipes,
        }


def connect_db(app):
    """connects database to flask app"""
    db.app = app
    db.init_app(app)