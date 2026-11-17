import os
from dotenv import load_dotenv
from app import create_app

# Load environment variables
load_dotenv()

# Create application instance with environment config
env = os.environ.get('FLASK_CONFIG', 'production')
app = create_app(env)

if __name__ == '__main__':
    app.run()
