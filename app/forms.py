from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Optional


class PostForm(FlaskForm):
    """Flask-WTF Form for creating and editing blog posts."""
    title = StringField('Title', validators=[
        DataRequired(message='Post title is required.'),
        Length(min=3, max=140, message='Title must be between 3 and 140 characters.')
    ])
    category_id = SelectField('Category', coerce=int, validators=[Optional()])
    tags = StringField('Tags (comma separated)', validators=[
        Optional(),
        Length(max=100, message='Tags string must not exceed 100 characters.')
    ])
    content = TextAreaField('Content', validators=[
        DataRequired(message='Content is required.')
    ])
    submit = SubmitField('Publish Post')


class CategoryForm(FlaskForm):
    """Flask-WTF Form for creating categories."""
    name = StringField('Category Name', validators=[
        DataRequired(message='Category name is required.'),
        Length(max=64, message='Category name cannot exceed 64 characters.')
    ])
    description = TextAreaField('Description', validators=[
        Optional(),
        Length(max=255, message='Description cannot exceed 255 characters.')
    ])
    submit = SubmitField('Create Category')


class CommentForm(FlaskForm):
    """Flask-WTF Form for post comments."""
    content = TextAreaField('Comment', validators=[
        DataRequired(message='Comment cannot be empty.'),
        Length(min=2, max=1000, message='Comment must be between 2 and 1000 characters.')
    ])
    submit = SubmitField('Submit Comment')


class DeleteForm(FlaskForm):
    """Flask-WTF CSRF-protected delete confirmation form."""
    submit = SubmitField('Delete')
