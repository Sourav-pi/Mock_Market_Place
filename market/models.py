from market import db, bcrypt, login_manager
from flask_login import UserMixin
from flask import redirect,url_for,flash

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    # return User.get(user_id)

class User(db.Model,UserMixin):
    id = db.Column(db.Integer(),primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address =db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(),nullable=False,default=1000)
    items = db.relationship('Item',backref='owned_user',lazy=True)

    @property
    def beautiful_budget(self):
        if(len(str(self.budget))>3):
            return str(self.budget)[:-3]+','+str(self.budget)[-3:]
        else :
            return str(self.budget)

    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self,plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
    
    def check_password_correction(self,attempted_password):
        return bcrypt.check_password_hash(self.password_hash,attempted_password)
    def can_buy(self, item):
        return self.budget >=item.price


    def __repr__(self):
        return f'User {self.username}'

class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=80), unique=True, nullable=False, primary_key=False)
    price = db.Column(db.Integer, nullable=False)
    barcode = db.Column(db.String(length=12), unique=True, nullable=False)
    description = db.Column(db.String(length=1024), unique=True, nullable=False)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def buy(self,buyer_user):
        self.owner = buyer_user.id
        buyer_user.budget -= self.price
        db.session.commit()
    
    def sell(self):
        owner = User.query.filter_by(id=self.owner).first()
        self.owner = None
        owner.budget += self.price
        db.session.commit()

    def __repr__(self):
        return f'Item {self.name}'