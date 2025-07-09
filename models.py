
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()
class Tool(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(100), nullable=True)
    slug = db.Column(db.String(100), unique=True)
    description =  db.Column(db.Text, nullable=True)
    url = db.Column(db.Text, nullable=True)
    lucide_icon = db.Column(db.Text, nullable = True)
    is_premium =  db.Column(db.Boolean, default = True)

    def __repr__(self):
        return f"<Tool {self.name}>"
    
class User(db.Model, UserMixin):
    id= db.Column(db.Integer,primary_key=True)
    username= db.Column(db.String(100),unique=True, nullable=False)
    email= db.Column(db.String(150), unique=True, nullable=False)
    password_hash= db.Column(db.String(256),nullable =False)
    role= db.Column(db.String(50), default="user")
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash,password)
    def is_admin(self):
        return self.role in ["admin", "superadmin"]
    def is_writer(self):
        return self.role in ["writer", "admin", "superadmin"]

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer,db.ForeignKey('user.id',name='fk_post_user'), nullable=False)
    created_at = db.Column(db.DateTime,default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,onupdate=datetime.utcnow)
    author = db.relationship('User', backref='posts')

