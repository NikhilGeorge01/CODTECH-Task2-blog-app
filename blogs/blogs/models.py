from blogs import db
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import desc
from hashlib import md5
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))  # Store the hashed password
    bio = db.Column(db.Text)
    posts = db.relationship('Post', backref="user", lazy='dynamic')

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def avatar(self,size):
        return "http://www.gravatar.com/avatar/{}?d=mm&s={}".format(md5(self.email.encode('utf-8')).hexdigest(),size)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        print("password is: ", password)
        print(f"Password hashed: {self.password_hash}") 
        print(check_password_hash(self.password_hash,password))

    def check_password(self, password):
      print(f"Stored password hash: {self.password_hash}")
      print(f"Password input to check: {password}")
      print(generate_password_hash(password))
      result = check_password_hash(self.password_hash, password)
      print(f"Password check result: {result}")
      return result

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)  # Call set_password to store the hashed password


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    postname = db.Column(db.String(120))
    content = db.Column(db.Text)
    last_modified = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Foreign key for user association

    @staticmethod
    def latest():
        return Post.query.order_by(desc(Post.last_modified)).all()
    
    

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __init__(self, postname, content, user_id, last_modified = None):
        self.postname = postname
        self.content = content
        self.user_id = user_id
        if last_modified is not None:
            self.last_modified = last_modified

