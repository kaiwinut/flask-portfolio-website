from flask import Blueprint, flash, redirect, render_template, request, url_for, jsonify
from flask_login import login_required, current_user
from server.models import User, Post, Comment, Like
from server import db

blogpage = Blueprint('blogpage', __name__)

@blogpage.route('/')
def blog():
    posts = Post.query.all()
    from server.config import CURRENT_YEAR
    return render_template('blog.html', user=current_user, posts=posts[::-1], current_year=CURRENT_YEAR)

@blogpage.route('/create-post/', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        text = request.form.get('text')
        if not text:
            flash('Post cannot be empty', category='error')
        elif not current_user.invited:
            flash('You have no permission to create posts', category='error')
        else:
            post = Post(text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post created!', category='success')
            return redirect(url_for('blogpage.blog'))

    return render_template('create_post.html', user=current_user)

@blogpage.route('/delete-post/<id>')
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()

    if not post:
        flash('Post does not exist.', category='error')
    elif current_user.id != post.author:
        flash('You do not have permission to delete this post.', category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted.', category='success')

    return redirect(url_for('blogpage.blog'))

@blogpage.route('/posts/<username>')
def posts(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash(f'No user with username: "{username}" exists.', category='error')
        return redirect(url_for('blogpage.blog'))

    posts = user.posts
    return render_template('posts.html', user=current_user, username=username, posts=posts[::-1])

@blogpage.route('/create-comment/<post_id>', methods=['POST'])
@login_required
def create_comment(post_id):
    text = request.form.get('text')

    if not text:
        flash('Comment cannot be empty!', category='error')
    else:
        post = Post.query.filter_by(id=post_id).first()
        if post:
            comment = Comment(text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('Post does not exist.', category='error')
        
    return redirect(url_for('blogpage.blog'))

@blogpage.route('/delete-comment/<comment_id>')
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        flash('Comment does not exist.', category='error')
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash('You have no permission to delete this comment.', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()
        
    return redirect(url_for('blogpage.blog'))

@blogpage.route('/like-post/<post_id>', methods=['POST'])
@login_required
def like(post_id):
    post = Post.query.filter_by(id=post_id).first()
    like = Like.query.filter_by(author=current_user.id, post_id=post_id).first()
    if not post:
        return jsonify({'error': 'Post does not exist.'}, 400)
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(author=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()

    return jsonify({'likes': len(post.likes), 'liked': current_user.id in map(lambda x: x.author, post.likes)})