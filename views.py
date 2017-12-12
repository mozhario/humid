import flask
from flask import render_template, Blueprint, redirect, request, flash, url_for
from flask_login import login_user, logout_user, login_required

from app import app, db
# from models import User
import models
import forms


views_bp = Blueprint('views_bp', __name__)


@app.route('/')
@login_required
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    valid =form.validate_on_submit()
    if form.validate_on_submit():
        user = models.User.query.filter_by(username=form.username.data).first()
        all_users = models.User.query.order_by(models.User.username).all()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or "/")

        flash('Invalid username or password.')
    # import pudb; pudb.set_trace()

    return render_template('auth/login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        user = models.User(email=form.email.data,
                            username=form.username.data,
                            password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You can now login.')
        return redirect(url_for('login'))
    return render_template('auth/register.html', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")
