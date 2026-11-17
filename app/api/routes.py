from flask import request, jsonify
from app.api import api_bp
from app.extensions import db
from app.models import User, Post

@api_bp.route('/users', methods=['GET'])
def get_users():
    """Retrieve all users."""
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200

@api_bp.route('/users', methods=['POST'])
def create_user():
    """Create a new user."""
    data = request.get_json() or {}
    username = data.get('username')
    email = data.get('email')

    if not username or not email:
        return jsonify({'error': 'username and email are required'}), 400

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({'error': 'Username or email already exists'}), 409

    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

@api_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Retrieve a single user."""
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict()), 200

@api_bp.route('/posts', methods=['GET'])
def get_posts():
    """Retrieve all blog posts."""
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return jsonify([post.to_dict() for post in posts]), 200

@api_bp.route('/posts', methods=['POST'])
def create_post():
    """Create a new blog post."""
    data = request.get_json() or {}
    title = data.get('title')
    content = data.get('content')
    user_id = data.get('user_id')

    if not title or not content or not user_id:
        return jsonify({'error': 'title, content, and user_id are required'}), 400

    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'error': 'Specified author (user) does not exist'}), 404

    post = Post(title=title, content=content, user_id=user_id)
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_dict()), 201

@api_bp.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """Retrieve a single blog post."""
    post = db.session.get(Post, post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    return jsonify(post.to_dict()), 200

@api_bp.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """Delete a blog post."""
    post = db.session.get(Post, post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404

    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'Post deleted successfully'}), 200
