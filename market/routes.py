from flask import render_template,redirect,url_for,flash, request
from market import app,db
from market.models import Item, User
from market.form import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from flask_login import login_user,logout_user,login_required, current_user

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market',methods=['GET','POST'])
@login_required
def market_page():
    items = Item.query.filter_by(owner=None)
    purchase_form = PurchaseItemForm()
    sell_form = SellItemForm()
    if request.method=='POST':
        print(request.form)
        purchased_item_name = request.form.get('purchased_item')
        purchased_item = Item.query.filter_by(name=purchased_item_name).first()
        if purchased_item :
            if current_user.can_buy(purchased_item):
                purchased_item.buy(current_user)
                flash(f'Congrats you have purchased {purchased_item.name}',category='success')
            else:
                flash(f"Sorry, currently you don't have engough funds to buy {purchased_item.name}",category='danger')
        sold_item_name = request.form.get('sold_item')
        sold_item = Item.query.filter_by(name=sold_item_name).first()
        if sold_item :
            sold_item.sell()
            flash(f'Congrats you have sold {sold_item.name}',category='success')
        return redirect(url_for('market_page'))
    if request.method=='GET':
        return render_template('market.html',items=items, purchase_form = purchase_form,sell_form=sell_form)

@app.route('/register',methods=['GET','POST'])
def register_page():
    form =RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data, email_address = form.email_address.data, password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Success !! You are logged in as : {current_user.username}',category='success')
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
    flash('You have been logged out !!',category='info')
    return redirect(url_for('home_page'))
