from flask import render_template,redirect,url_for,flash
from market import app,db
from market.models import Item, User
from market.form import RegisterForm
@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market')
def market_page():
    items = Item.query.all()
    return render_template('market.html',items=items)

@app.route('/register',methods=['GET','POST'])
def register_page():
    form =RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data, email_address = form.email_address.data, password_hash=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('market_page'))
    if(form.errors !={}):
        for err_msg in form.errors.values():
            if(err_msg[0]=="Field must be equal to password1."):
                err_msg[0]="Password and confirm password must match."
            flash(err_msg[0], category='danger')
    return render_template('register.html',form=form)