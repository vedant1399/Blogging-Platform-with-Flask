import os
from dotenv import load_dotenv
from app import create_app
from app.extensions import db
from app.models import User, Post, Category, Tag, Comment

# Load environment variables from .env file
load_dotenv()

app = create_app(os.getenv('FLASK_CONFIG', 'development'))

@app.shell_context_processor
def make_shell_context():
    """Make database and models accessible in flask shell."""
    return {
        'db': db,
        'User': User,
        'Post': Post,
        'Category': Category,
        'Tag': Tag,
        'Comment': Comment
    }

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
