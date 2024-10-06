from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User,Post
from . import app, lm, db
from .forms import LoginForm, SignupForm, UserProfileForm, AddPostForm
from datetime import datetime  # This imports the datetime class directly


@lm.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/')
def index():
    return render_template("index.html")

@login_required
@app.route('/home', methods=['GET', 'POST'])
def home():
    form = AddPostForm()
    posts = Post.query.filter_by(user_id=current_user.id).all()

    if form.validate_on_submit():
        new_post = Post(
            postname=form.post_name.data,
            content=form.content.data,
            user_id=current_user.id,
        )
        new_post.save()
        flash("Post was successful", "success")
        return redirect(url_for('home'))

    return render_template("home.html", form=form, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    print("starting ")
    form = LoginForm()
    print("ok")
    if form.validate_on_submit():
        print("Form validated!")  # Debugging line
        user = User.query.filter_by(email=form.email.data).first()  # Fetch user by email
        if user and user.check_password(form.password.data):  # Check password
            login_user(user, form.remember_me.data)  # Log in user
            flash("Login successful")  # Success message
            return redirect(url_for('home'))  # Redirect to home
        flash("Incorrect password or email")  # Flash error message
       
        with app.app_context():
          users = User.query.limit(5).all()
          
           # Print the errors that caused validation to fail
    return render_template("login.html", form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():  # Hash password
        new_user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()  # Save new user to the database
        flash("Registration successful, please log in.")
        return redirect(url_for('login'))
    else:
        print(form.errors)
    return render_template("signup.html", form=form)
@login_required
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/public' , methods=['GET', 'POST'])
@login_required
def public():
    posts = Post.latest()
    return render_template("public.html", posts=posts)

# Route to update a post
@app.route('/post/update/<int:post_id>', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)

    # Ensure the current user is the author of the post
    if post.user_id != current_user.id:
        flash('You are not authorized to update this post.', 'danger')
        return redirect(url_for('home'))  # Redirect to home if unauthorized

    if request.method == 'POST':
        post.content = request.form['content']  # Only update the post content
        post.save()  # Save the updated post to the database
        flash('Post updated successfully!', 'success')
        return redirect(url_for('home'))  # Redirect to home after updating

    # For GET request, render the update form with existing post content
    return render_template('update_post.html', post=post)
# Route to delete a post
@app.route('/post/delete/<int:post_id>', methods=['POST', 'GET'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    # Ensure the current user is the author of the post
    if post.user_id != current_user.id:
        flash('You are not authorized to delete this post.', 'danger')
        return redirect(url_for('home'))  # Redirect to home if unauthorized

    db.session.delete(post)  # Delete the post from the database
    db.session.commit()  # Commit the changes to the database
    flash('Post deleted successfully!', 'success')
    return redirect(url_for('home'))  # Redirect to home after deleting


