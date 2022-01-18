import os, sys
import shutil
import json

import random
from flask import (
    render_template,
    flash,
    redirect,
    url_for,
    request,
    abort,
    send_from_directory,
    session
    )
from flask_login import (
    current_user,
    login_user,
    logout_user,
    login_required
    )
from werkzeug.utils import secure_filename
from pathlib import Path
from sqlalchemy import desc
import requests

from project import app, db, logger
from project.forms import SignInForm, SignUpForm
from project.models import Channel, User, Track
from project.functions import validate_image, crop_and_resize, get_tags


@app.route('/profile_edit')
def profile_edit():
    user = current_user
    tracks = user.tracks.order_by(desc(Track.timestamp))
    return render_template('profile_edit.html', user=user, tracks=tracks, sidebar_tags=get_tags())


@login_required
@app.route('/profile_edit', methods=['POST'])
def upload_files():
    # Delete tracks from user's library
    tracks = current_user.tracks.order_by(desc(Track.timestamp))
    for track_number in request.form.getlist('checkbox')[::-1]:
        track = tracks[int(track_number) - 1]
        db.session.delete(track)
        db.session.commit()
    # Set path for saving pictures
    file_path = Path(
        app.config['UPLOAD_PATH'] + current_user.username + '1.png')
    file_path2 = Path(
        app.config['UPLOAD_PATH'] + current_user.username + '2.png')
    file_path3 = Path(
        app.config['UPLOAD_PATH'] + current_user.username + '3.png')
    # Get bio, number and uploaded file from the form
    bio = request.form.get('bio')
    number = request.form.get('number').lstrip('0')
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    current_user.bio = bio
    # Delete old profile images
    if (number != '0' and number != '') or filename != '':
        if file_path2.exists():
            os.rename(file_path2, file_path3)
        if file_path.exists():
            os.rename(file_path, file_path2)
    # Choose profile picture from library
    if number != '0' and number != '':
        shutil.copyfile(
            app.config['PROFILE_PICS'] + number + '.jpg',
            app.config['UPLOAD_PATH'] + current_user.username + '1.png')
    # Upload image, validate it, then resize, crop and save
    if filename != '':
        file_ext = os.path.splitext(filename)[-1]
        if file_ext == '.jpeg':
            file_ext = '.jpg'

        if (file_ext not in app.config['UPLOAD_EXTENSIONS']
                or file_ext != validate_image(uploaded_file.stream)):
            abort(400)
        resized_file = crop_and_resize(uploaded_file)
        resized_file.save(
            os.path.join(
                app.config['UPLOAD_PATH'],
                (current_user.username + '1.png')
                )
            )
    db.session.commit()
    return redirect(url_for('profile_edit'))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/home')
def home():
    return render_template('about.html', sidebar_tags=get_tags())


@app.route('/channel/<number>')
def channel(number):
    # Get random selection of tags for the channel
    channel = Channel.query.get(number)
    tags_list = channel.tags.split(', ')
    tags = ', '.join(random.sample(tags_list, 8))
    while len(tags) > 140:
        tags = ', '.join(random.sample(tags_list, 8))
    return render_template('channel.html', channel=channel, tags=tags, sidebar_tags=get_tags())


@login_required
@app.route('/background_save/<number>')
def background_save(number):
    """
    Save playing track to user's library
    """
    logger.info('save entered')
    r = requests.get('http://icecast:8090/status-json.xsl')
    logger.info('got a request')
    data = json.loads(r.text)
    logger.info('data', data)
    data = json.loads(data['icestats']['source'][int(number) - 1]['title'][3:])
    logger.info('data2', data)
    artist = data['artist']
    album = data['album']
    year = data['year']
    title = data['song_title']
    label = data['label']
    path = data['path']
    channel = number
    already_exists = Track.query.filter_by(
        artist=artist, song_title=title,
        year=year, album_title=album, path=path,
        label=label, user_id=current_user.id,
        channel=channel
    ).first() is not None
    if not already_exists:
        track = Track(
            artist=artist, song_title=title,
            year=year, album_title=album, path=path,
            label=label, user_id=current_user.id
        )
        db.session.add(track)
        db.session.commit()
        return 'OK'
    return 'Track already added'


@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    logger.info('sign_in entered')
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            logger.info('Invalid username or password')
            flash('Invalid username or password')
            return redirect(url_for('sign_in'))
        login_user(user)
        logger.info('sign_up excess')
        return redirect(url_for('profile', username=current_user.username))
    return render_template('sign_in.html', title='Sign In', form=form)


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        for i in range(1, 4):
            shutil.copyfile(
                app.config['PROFILE_PICS'] +
                str(random.randrange(1, 228)) + '.jpg',
                app.config['UPLOAD_PATH'] +
                user.username + f'{i}.png'
            )
        return redirect(url_for('sign_in'))
    return render_template('sign_up.html', title='Sing up', form=form)


@app.route('/log_out')
@login_required
def log_out():
    logout_user()
    return redirect(url_for('index'))


@app.route('/user/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    tracks = user.tracks.order_by(desc(Track.timestamp))
    bio = user.bio
    return render_template('profile.html', user=user, tracks=tracks, bio=bio, sidebar_tags=get_tags())


@app.route('/uploads/<filename>/<number>')
def profile_pic(filename, number):
    """
    Serve static files (profile pictures)
    """
    return send_from_directory(
        app.config['UPLOAD_PATH'], filename + f'{number}.png')


@app.errorhandler(404)
def page_not_found(e):
    number = random.randrange(1, 3)
    return render_template('404.html', number=number), 404


@app.errorhandler(500)
def page_not_found(e):
    number = random.randrange(1, 3)
    return render_template('404.html', number=number), 500


@app.route("/static/<path:filename>")
def staticfiles(filename):
    return send_from_directory(app.config["STATIC_FOLDER"], filename)


@app.route("/covers/<path:filename>")
def coversfiles(filename):
    return send_from_directory(app.config["COVERS_FOLDER"], filename)


@app.route("/media/<path:filename>")
def mediafiles(filename):
    return send_from_directory(app.config["MEDIA_FOLDER"], filename)
