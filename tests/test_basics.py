import unittest
from app import create_app
from app.extensions import db
from app.models import User, Post

class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test client and create clean test database."""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        """Tear down database and pop context."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        """Verify that application instance was created."""
        self.assertFalse(self.app is None)

    def test_app_is_testing(self):
        """Verify that app is running in testing mode."""
        self.assertTrue(self.app.config['TESTING'])

    def test_health_check(self):
        """Verify health check endpoint returns 200."""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertEqual(json_data['status'], 'healthy')

    def test_index_page(self):
        """Verify index route renders properly."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Blogging Platform', response.data)

    def test_user_and_post_models(self):
        """Verify SQLAlchemy ORM models and relationships."""
        # Create user
        user = User(username='blogger', email='blogger@example.com')
        db.session.add(user)
        db.session.commit()

        # Query user
        saved_user = User.query.filter_by(username='blogger').first()
        self.assertIsNotNone(saved_user)
        self.assertEqual(saved_user.email, 'blogger@example.com')

        # Create post associated with user
        post = Post(title='My First Blog Post', content='Hello World!', user_id=saved_user.id)
        db.session.add(post)
        db.session.commit()

        # Verify relationship
        self.assertEqual(saved_user.posts.count(), 1)
        self.assertEqual(saved_user.posts.first().title, 'My First Blog Post')
        self.assertEqual(post.author.username, 'blogger')

    def test_api_user_creation(self):
        """Verify POST /api/users endpoint."""
        response = self.client.post('/api/users', json={
            'username': 'apiuser',
            'email': 'apiuser@example.com'
        })
        self.assertEqual(response.status_code, 201)
        json_data = response.get_json()
        self.assertEqual(json_data['username'], 'apiuser')

        # Verify duplicate prevention
        dup_response = self.client.post('/api/users', json={
            'username': 'apiuser',
            'email': 'apiuser@example.com'
        })
        self.assertEqual(dup_response.status_code, 409)

    def test_api_post_creation(self):
        """Verify POST /api/posts and GET /api/posts."""
        # First create an author
        user_res = self.client.post('/api/users', json={
            'username': 'author1',
            'email': 'author1@example.com'
        })
        user_id = user_res.get_json()['id']

        # Create post
        post_res = self.client.post('/api/posts', json={
            'user_id': user_id,
            'title': 'Test Post Title',
            'content': 'Test Post Content Body'
        })
        self.assertEqual(post_res.status_code, 201)
        post_data = post_res.get_json()
        self.assertEqual(post_data['title'], 'Test Post Title')
        self.assertEqual(post_data['author'], 'author1')

        # Get posts
        get_res = self.client.get('/api/posts')
        self.assertEqual(get_res.status_code, 200)
        posts_list = get_res.get_json()
        self.assertGreaterEqual(len(posts_list), 1)


if __name__ == '__main__':
    unittest.main()
