from bachelor_kitchen import app, db, bcrypt
from flask import render_template, url_for, flash, redirect, request, session, send_from_directory, make_response
from flask_login import login_user, current_user, logout_user, login_required
from bachelor_kitchen.forms import RegistrationForm, LoginForm
from bachelor_kitchen.models import User


@app.route("/", methods=['GET'])
@app.route("/home", methods=['GET'])
def home():
    return render_template('layout.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=form.password.data,
                    firstname=form.firstname.data,
                    lastname=form.lastname.data,
                    phonenum=form.phonenum.data,
                    address=form.address.data,
                    city=form.city.data,
                    zipcode=form.zipcode.data,
                    state=form.state.data,
                    dob=form.dob.data,
                    university=form.university.data
                    )
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('register'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user, remember=False)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))
