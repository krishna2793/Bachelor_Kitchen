from bachelor_kitchen import app,db
from flask import render_template, url_for, flash, redirect, request,session, send_from_directory, make_response
from flask_login import login_user, current_user, logout_user, login_required
from bachelor_kitchen.forms import RegistrationForm
from bachelor_kitchen.models import User





@app.route("/", methods=['GET'])
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
            city = form.city.data,
            zipcode = form.zipcode.data,
            state = form.state.data,
            dob=form.dob.data,
            university = form.university.data
            )
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('register'))
    return render_template('register.html', title='Register', form=form)