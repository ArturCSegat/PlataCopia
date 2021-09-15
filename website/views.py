from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask.helpers import url_for
from flask_login import login_required, current_user
from sqlalchemy.orm import query
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.functions import user
from .models import Post, User, ImagePost, Room
from . import db


views = Blueprint("views", __name__)

@views.route('/')
@views.route('/home')
@login_required
def home():

    posts = Post.query.all()
    image_posts = ImagePost.query.all()
    rooms = Room.query.all()

    return render_template("index.html",user=current_user, posts=posts, images=image_posts, rooms=rooms)

@views.route('/create-room', methods =['GET', 'POST'])
@login_required
def create_room():
    if request.method == 'POST':
        
        title = request.form.get('title')
        info = request.form.get('info')


        if not text or not info:
            flash('Post cannot be empty', category='error')

        else:
            new_room = Room(title=title, info=info, author=current_user.id)

            db.session.add(new_room)
            db.session.commit()

            flash('Room created', category='success')
            return redirect(url_for('views.home'))

    return render_template('create-room.html', user=current_user)

@views.route('/create-post', methods =['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        
        title = request.form.get('title')
        text = request.form.get('text')

        if not text:
            flash('Post cannot be empty', category='error')

        else:
            new_post = Post(text=str(text), author=current_user.id, title=title, )

            db.session.add(new_post)
            db.session.commit()

            flash('Post posted', category='success')
            return redirect(url_for('views.home'))

    return render_template('create-post.html', user=current_user)

@views.route('/image-post', methods =['GET', 'POST'])
@login_required
def create_image_post():
    if request.method == 'POST':

        title = request.form.get('title')
        link = request.form.get('link')
        caption = request.form.get('text')

        if not link:
            flash('Post cannot be empty', category='error')

        else:
            if caption != "default caption":
                new_post = ImagePost(img=link, author=current_user.id, title=title, cp=caption)
            else:
                new_post = ImagePost(img=link, author= current_user, title=title)

            db.session.add(new_post)
            db.session.commit()

            flash('Post posted', category='success')
            return redirect(url_for('views.home'))

    return render_template('image-post.html', user=current_user)

@views.route('/delete-post/<id>')
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()
   
    if not post:
        flash("This post does not exist", category='error')
        return redirect(url_for('views.home'))
    elif current_user.id != post.author:
        flash("You cannot delete someone elses's post", category='error')
        return redirect(url_for('views.home'))
    else:
        db.session.delete(post)
        db.session.commit()
        flash('post deleted successfuly', category='success')
        return redirect(url_for('views.home'))

@views.route('/delete-image/<id>')
@login_required
def delete_image(id):
    image = ImagePost.query.filter_by(id=id).first()
   
    if not image:
        flash("This post does not exist", category='error')
        return redirect(url_for('views.home'))
    elif current_user.id != image.author:
        flash("You cannot delete someone elses's post", category='error')
        return redirect(url_for('views.home'))
    else:
        db.session.delete(image)
        db.session.commit()
        flash('Post deleted successfuly', category='success')
        return redirect(url_for('views.home'))

@views.route('/delete-room/<id>')
@login_required
def delete_room(id):
    room = Room.query.filter_by(id=id).first()
   
    if not room:
        flash("This room does not exist", category='error')
        return redirect(url_for('views.home'))
    elif current_user.id != room.author:
        flash("You cannot delete someone elses's room", category='error')
        return redirect(url_for('views.home'))
    else:
        db.session.delete(room)
        db.session.commit()
        flash('post deleted successfuly', category='success')
        return redirect(url_for('views.home'))

        


@views.route('/posts/<username>')
@login_required
def user_profile_posts(username):
    user =User.query.filter_by(username=username).first()

    if not user:
        flash('This user does no exist', category='error')
        return redirect(url_for('views.home'))

    posts = Post.query.filter_by(author=user.id).all()
    images = ImagePost.query.filter_by(author=user.id).all()
    return render_template("posts.html", user=current_user, posts=posts, images=images, username=username)

@views.route('/rooms/<username>')
@login_required
def user_profile_rooms(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('This user does no exist', category='error')
        return redirect(url_for('views.home'))

    rooms = Room.query.filter_by(author=user.id).all()

    return render_template("rooms.html", user=current_user, rooms=rooms, username=username)

@views.route('/content/<room>')
@login_required
def room_content(room):

    room = int(room)
    
    current_room = Room.query.filter_by(id=room).first()

    if not current_room:
         flash('This room does no exist', category='error')
    else:

        images = ImagePost.query.filter_by(parent=current_room.id).all()
        posts = Post.query.filter_by(parent=current_room.id).all()



    return render_template("room-content.html", user=current_user, posts=posts, images=images, username=current_room.title, info =current_room.info)


