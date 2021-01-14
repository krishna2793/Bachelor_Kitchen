from bachelor_kitchen import app, db, bcrypt, mail
from flask import render_template, url_for, flash, redirect, request, session, send_from_directory, make_response, abort
from flask_login import login_user, current_user, logout_user, login_required
from bachelor_kitchen.forms import RegistrationForm, LoginForm, PostForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm, UpdatePostForm
from bachelor_kitchen.models import User, Post, ReservedPost
from PIL import Image
import secrets
import os
from flask_mail import Message
import stripe
import time

stripe_keys = {
    'secret_key': os.environ['STRIPE_SECRET_KEY'],
    'publishable_key': os.environ['STRIPE_PUBLISHABLE_KEY']
}

stripe.api_key = stripe_keys['secret_key']



@app.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@app.route("/admin/home", methods=['GET', 'POST'])
@login_required
def adminhome():
    if current_user.username != "admin":
        return redirect(url_for('home'))
    page = request.args.get('page', 1, type=int)
    users = User.query.all()
    return render_template('view_all_users.html', title='View all Users', users=users)



@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
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
                    university="ASU"

                    )
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/", methods=['GET', 'POST'])
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
            if current_user.username == "admin":
                return redirect(url_for('adminhome'))
            else:
                return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    content=form.content.data, author=current_user, cookingdate=form.cookingdate.data, cost=form.cost.data,time = form.time.data, deadline=form.deadline.data, entries=form.entries.data)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.phonenum = form.phonenum.data
        current_user.profile = form.profile.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.phonenum.data = current_user.phonenum
    image_file = url_for(
        'static', filename='profile_pics/' + current_user.image_file)
    return render_template('profile.html', title='Profile',
                           image_file=image_file, form=form)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post, key=stripe_keys['publishable_key'])


@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = UpdatePostForm()
    if form.validate_on_submit():
        post.cookingdate=form.cookingdate.data
        post.content = form.content.data
        post.entries=form.entries.data
        post.deadline=form.deadline.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.content.data = post.content
        form.entries.data = post.entries
        form.cookingdate.data = post.cookingdate
        form.deadline.data = post.deadline
    return render_template('update.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/post/<int:post_id>/reserve", methods=['POST'])
@login_required
def reserve(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author == current_user:
        abort(403)
    rpost = ReservedPost.query.filter_by(
        originalpostid=post.postid, registereduser=current_user.username).first()
    if rpost is not None:
        flash('You already reserved the slot', 'danger')
        return redirect(url_for('home'))
    try:
        amount = post.cost*100   # amount in cents
        customer = stripe.Customer.create(
            email=current_user.email,
            source=request.form['stripeToken']
        )
        stripe.Charge.create(
            customer=customer.id,
            amount=amount,
            currency='usd',
            description=post.title
        )
        post.author.balance += post.cost
        post.entries -= 1
        db.session.commit()
        post1 = ReservedPost(title=post.title, originalpostid=post.postid,
                             content=post.content, author1=current_user, cookingdate=post.cookingdate, cost=post.cost, deadline=post.deadline, entries=post.entries)
        db.session.add(post1)
        db.session.commit()
        flash('You have successfully registered your slot', 'success')
        return redirect(url_for('home'))
    except stripe.error.StripeError:
        return render_template('error.html')


@app.route("/reservedslots/user/<string:username>")
def reserved_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = ReservedPost.query.filter_by(author1=user)\
        .order_by(ReservedPost.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('reserved_posts.html', posts=posts, user=user)


@app.route("/view_registered_users/<int:post_id>", methods=['GET', 'POST'])
@login_required
def view_registered_users(post_id):
    posts = ReservedPost.query.filter_by(originalpostid=post_id).all()
    # print(posts)
    # print(posts[0].registereduser.firstname)
    return render_template('view_registered_users.html', title='View Registered Users', posts=posts)


@app.route("/directions/<int:post_id>", methods=['GET'])
def directions(post_id):
    post = Post.query.get_or_404(post_id)
    user = User.query.filter_by(username=post.author.username).first()
    source = " ".join([current_user.address, current_user.city, current_user.state, current_user.zipcode])
    destination = " ".join([user.address, user.city, user.state, user.zipcode])
    return render_template('directions.html', source=source, destination=destination)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender=app.config['MAIL_USERNAME'],
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.password = form.password.data
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)


def busy_wait(dt):
    current_time = time.time()
    while(time.time() < current_time+dt):
        pass

@app.route("/dummy", methods=['GET'])
def dummy():
    busy_wait(5)
    return render_template('error.html')