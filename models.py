from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
import secrets

# Assuming these are initialized somewhere in your application
login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String(36), primary_key=True, default=uuid.uuid4().hex)
    first_name = db.Column(db.String(150), nullable=True, default='')
    last_name = db.Column(db.String(150), nullable=True, default='')
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=True, default='')
    g_auth_verify = db.Column(db.Boolean, default=False)
    token = db.Column(db.String(32), default='', unique=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Fighter(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: uuid.uuid4().hex)
    name = db.Column(db.String(100), nullable=False)
    origin = db.Column(db.String(100), nullable=False)
    special_move = db.Column(db.String(100))

    def __repr__(self):
        return f'Fighter(id={self.id}, name={self.name}, origin={self.origin}, special_move={self.special_move})'

class FighterSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'origin', 'special_move']

fighter_schema = FighterSchema()
fighters_schema = FighterSchema(many=True)
