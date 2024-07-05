from flask import render_template,redirect,url_for,flash
from market import app,db
from market.models import Item, User
from market.form import RegisterForm, LoginForm
from flask_login import login_user,logout_user

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
        user_to_create = User(username=form.username.data, email_address = form.email_address.data, password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('market_page'))
    if(form.errors !={}):
        for err_msg in form.errors.values():
            if(err_msg[0]=="Field must be equal to password1."):
                err_msg[0]="Password and confirm password must match."
            flash(err_msg[0], category='danger')
    return render_template('register.html',form=form)

@app.route('/login',methods=['GET','POST'])
def login_page():
    form=LoginForm()
    if(form.validate_on_submit()):
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if (attempted_user and attempted_user.check_password_correction(form.password.data)):
            login_user(attempted_user)
            flash(f'Success !! You are logged in as : {attempted_user.username}',category='success')
            return redirect(url_for('market_page'))
        else :
            flash(f"Username and password don't match",category='danger')


    return render_template('login.html',form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash('You have been logged out !!')
    return redirect(url_for('home_page'))
