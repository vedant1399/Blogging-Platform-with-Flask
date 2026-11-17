from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app.posts import posts_bp
from app.extensions import db
from app.models import Post, Category, Tag, Comment
from app.forms import PostForm, CategoryForm, CommentForm, DeleteForm


def get_category_choices():
    """Helper to populate category dropdown choices."""
    categories = Category.query.order_by(Category.name).all()
    return [(0, 'Uncategorized')] + [(c.id, c.name) for c in categories]


@posts_bp.route('/')
def list_posts():
    """List all blog posts with paginated navigation, category and tag filters."""
    page = request.args.get('page', 1, type=int)
    per_page = 6
    pagination = Post.query.order_by(Post.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    posts = pagination.items
    categories = Category.query.order_by(Category.name).all()
    tags = Tag.query.order_by(Tag.name).all()
    return render_template('posts/list.html', pagination=pagination, posts=posts, categories=categories, tags=tags)


@posts_bp.route('/new', methods=['GET', 'POST'])
@login_required
def create_post():
    """Create a new blog post using Flask-WTF and Rich Text Editor."""
    form = PostForm()
    form.category_id.choices = get_category_choices()

    if form.validate_on_submit():
        category_id = form.category_id.data if form.category_id.data != 0 else None
        post = Post(
            title=form.title.data.strip(),
            content=form.content.data,
            user_id=current_user.id,
            category_id=category_id
        )
        if form.tags.data:
            post.set_tags_from_string(form.tags.data)

        db.session.add(post)
        db.session.commit()
        flash(f'Post "{post.title}" published successfully!', 'success')
        return redirect(url_for('posts.post_detail', post_id=post.id))

    return render_template('posts/create.html', form=form, title='Create New Post')


@posts_bp.route('/<int:post_id>')
def post_detail(post_id):
    """View a single blog post in detail with comments, breadcrumbs & navigation."""
    post = db.session.get(Post, post_id)
    if not post:
        abort(404)
    delete_form = DeleteForm()
    comment_form = CommentForm()
    prev_post = Post.query.filter(Post.id < post.id).order_by(Post.id.desc()).first()
    next_post = Post.query.filter(Post.id > post.id).order_by(Post.id.asc()).first()
    return render_template(
        'posts/detail.html',
        post=post,
        delete_form=delete_form,
        comment_form=comment_form,
        prev_post=prev_post,
        next_post=next_post
    )


@posts_bp.route('/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    """Edit an existing post (Author only)."""
    post = db.session.get(Post, post_id)
    if not post:
        abort(404)
    if post.author != current_user:
        flash('You are not authorized to edit this post.', 'danger')
        return redirect(url_for('posts.post_detail', post_id=post.id))

    form = PostForm()
    form.category_id.choices = get_category_choices()

    if form.validate_on_submit():
        post.title = form.title.data.strip()
        post.content = form.content.data
        post.category_id = form.category_id.data if form.category_id.data != 0 else None
        post.set_tags_from_string(form.tags.data)

        db.session.commit()
        flash(f'Post "{post.title}" updated successfully!', 'success')
        return redirect(url_for('posts.post_detail', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.category_id.data = post.category_id or 0
        form.tags.data = post.get_tags_string()

    return render_template('posts/create.html', form=form, title=f'Edit: {post.title}', is_edit=True, post=post)


@posts_bp.route('/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    """Delete a blog post (Author only)."""
    post = db.session.get(Post, post_id)
    if not post:
        abort(404)
    if post.author != current_user:
        flash('You are not authorized to delete this post.', 'danger')
        return redirect(url_for('posts.post_detail', post_id=post.id))

    delete_form = DeleteForm()
    if delete_form.validate_on_submit():
        title = post.title
        db.session.delete(post)
        db.session.commit()
        flash(f'Post "{title}" has been deleted.', 'info')
        return redirect(url_for('posts.list_posts'))

    flash('Invalid delete request.', 'danger')
    return redirect(url_for('posts.post_detail', post_id=post.id))


@posts_bp.route('/<int:post_id>/comments', methods=['POST'])
@login_required
def add_comment(post_id):
    """Add a new comment to a post (Authenticated users only)."""
    post = db.session.get(Post, post_id)
    if not post:
        abort(404)

    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(
            content=form.content.data.strip(),
            user_id=current_user.id,
            post_id=post.id
        )
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been posted!', 'success')
    else:
        for error in form.content.errors:
            flash(error, 'danger')

    return redirect(url_for('posts.post_detail', post_id=post.id) + '#comments')


@posts_bp.route('/comments/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    """Delete a comment (Comment author or Post author only)."""
    comment = db.session.get(Comment, comment_id)
    if not comment:
        abort(404)

    post_id = comment.post_id
    # Authorization: Either the comment author or the post owner can delete
    if comment.author != current_user and comment.post.author != current_user:
        flash('You are not authorized to delete this comment.', 'danger')
        return redirect(url_for('posts.post_detail', post_id=post_id) + '#comments')

    delete_form = DeleteForm()
    if delete_form.validate_on_submit():
        db.session.delete(comment)
        db.session.commit()
        flash('Comment deleted.', 'info')
    else:
        flash('Invalid request.', 'danger')

    return redirect(url_for('posts.post_detail', post_id=post_id) + '#comments')


@posts_bp.route('/category/<slug>')
def category_posts(slug):
    """Filter posts by category with pagination."""
    category = Category.query.filter_by(slug=slug).first_or_404()
    page = request.args.get('page', 1, type=int)
    per_page = 6
    pagination = category.posts.order_by(Post.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    posts = pagination.items
    return render_template('posts/category.html', category=category, pagination=pagination, posts=posts)


@posts_bp.route('/tag/<slug>')
def tag_posts(slug):
    """Filter posts by tag with pagination."""
    tag = Tag.query.filter_by(slug=slug).first_or_404()
    page = request.args.get('page', 1, type=int)
    per_page = 6
    pagination = tag.posts.order_by(Post.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    posts = pagination.items
    return render_template('posts/tag.html', tag=tag, pagination=pagination, posts=posts)


@posts_bp.route('/categories', methods=['GET', 'POST'])
@login_required
def manage_categories():
    """Create and list categories."""
    form = CategoryForm()
    if form.validate_on_submit():
        name = form.name.data.strip()
        if Category.query.filter_by(name=name).first():
            flash(f'Category "{name}" already exists.', 'warning')
        else:
            cat = Category(name=name, description=form.description.data)
            db.session.add(cat)
            db.session.commit()
            flash(f'Category "{cat.name}" created successfully!', 'success')
            return redirect(url_for('posts.manage_categories'))

    categories = Category.query.order_by(Category.name).all()
    return render_template('posts/categories.html', form=form, categories=categories)
