import datetime

import requests
from flask import request, redirect, render_template
from flask_login import login_user, login_required, logout_user, current_user
from flask_wtf import Form, FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form

from app import app, db, login_manager, bcrypt
from app.forms import EventForm, LoginForm, CreateUserForm, LogoutForm, EventDeleteForm
from app.models import Event, User


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)



@app.route("/", methods=["GET"])
def main():
    events = Event.query.order_by(Event.datetime_start).all()
    return render_template('main.html', events=events)



@app.route('/event', methods=['POST', 'GET'])
@login_required
def event():
    event_form = EventForm()
    if request.method == 'POST':
        user_id = current_user.get_id()
        datetime_start = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        datetime_end = datetime.datetime.strptime(request.form.get('datetime_end'), '%m/%d/%Y %I:%M %p').strftime('%Y-%m-%d %H:%M:%S')
        topic = request.form.get('topic')
        description = request.form.get('description')

        event = Event(user_id=user_id,
                      datetime_start=datetime_start,
                      datetime_end=datetime_end,
                      topic=topic,
                      description=description
                      )

        db.session.add(event)
        db.session.commit()
        return redirect('/')
    return render_template('add_event.html', form=event_form)


@app.route('/event/<id>', methods=['GET', 'POST'])
@login_required
def event_editor(id):
    event = Event.query.get_or_404(id)
    form = EventForm(obj=event)
    if request.method == 'POST':
        if current_user == event.user_id:
            form.populate_obj(event)
            db.session.add(event)
            db.session.commit()
        return redirect("/")
    return render_template('event_edit.html', event=event, form=form)


@app.route('/event/delete/<id>', methods=['POST', 'GET'])
@login_required
def delete_event(id):
    event = Event.query.get_or_404(id)
    if int(current_user.get_id()) == event.user_id:
        form = EventDeleteForm()
        if request.method == 'POST':
            if form.delete_or_not.data:
                db.session.delete(event)
                db.session.commit()
                return redirect("/")
        return render_template('event_delete.html', event=event, form=form)
    return redirect("/")


@app.route("/sing-in", methods=["GET", "POST"])
def create_user():
    if current_user.is_anonymous:
        form = CreateUserForm()
        if form.validate_on_submit():
            username = request.form.get('username')
            password = request.form.get('password')
            user = User(username=username, password=bcrypt.generate_password_hash(password).decode('utf-8'))
            user.authenticated = True
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True)
            return redirect("/")
        return render_template("sing_in.html", form=form)
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_anonymous:
        form = LoginForm()
        if form.validate_on_submit():
            username = request.form.get('username')
            password = request.form.get('password')
            user = User.query.filter_by(username=username).first_or_404(
                description='There is no data with {}'.format(username))
            if user:
                if bcrypt.check_password_hash(user.password, password):
                    user.authenticated = True
                    db.session.add(user)
                    db.session.commit()
                    login_user(user, remember=True)
                    return redirect("/")
        return render_template('login.html', form=form)
    return redirect("/")


@app.route("/logout", methods=['POST', 'GET'])
@login_required
def logout():
    form = LogoutForm()
    if request.method == 'POST':
        if form.logout_or_not.data:
            logout_user()
            return redirect('/')
        return redirect('/')
    return render_template('logout.html', form=form)
