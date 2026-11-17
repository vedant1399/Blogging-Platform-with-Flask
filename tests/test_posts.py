import unittest
from app import create_app
from app.extensions import db
from app.models import User, Post, Category, Tag
from app.forms import PostForm, CategoryForm


class PostCRUDTestCase(unittest.TestCase):
    def setUp(self):
        """Set up testing app and in-memory test database."""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

        # Create two authors for permissions testing
        self.author1 = User(username='alice', email='alice@example.com')
        self.author1.set_password('password123')
        self.author2 = User(username='bob', email='bob@example.com')
        self.author2.set_password('password123')
        db.session.add_all([self.author1, self.author2])
        db.session.commit()

        # Create a sample category
        self.category = Category(name='Technology', description='Tech articles')
        db.session.add(self.category)
        db.session.commit()

    def tearDown(self):
        """Tear down database and application context."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login(self, username='alice', password='password123'):
        """Helper to log in a user (logs out first)."""
        self.client.get('/auth/logout')
        return self.client.post('/auth/login', data={
            'identifier': username,
            'password': password
        }, follow_redirects=True)

    def test_category_and_tag_models(self):
        """Verify Category and Tag creation and relationship with Post."""
        post = Post(
            title='Understanding Flask-WTF',
            content='This is a detailed guide on Flask-WTF and SQLAlchemy.',
            user_id=self.author1.id,
            category_id=self.category.id
        )
        post.set_tags_from_string('flask, python, web')
        db.session.add(post)
        db.session.commit()

        # Verify Category relation
        self.assertEqual(post.category.name, 'Technology')
        self.assertEqual(self.category.posts.count(), 1)

        # Verify Tags relation
        self.assertEqual(len(post.tags), 3)
        tag_names = [t.name for t in post.tags]
        self.assertIn('flask', tag_names)
        self.assertIn('python', tag_names)
        self.assertIn('web', tag_names)

    def test_create_post_authenticated(self):
        """Verify authenticated user can create a post via /posts/new."""
        self.login('alice')
        response = self.client.post('/posts/new', data={
            'title': 'New Flask Post',
            'content': '<p>This is rich HTML content created via Quill.</p>',
            'category_id': self.category.id,
            'tags': 'tutorial, backend'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'New Flask Post', response.data)

        # Verify in DB
        post = Post.query.filter_by(title='New Flask Post').first()
        self.assertIsNotNone(post)
        self.assertEqual(post.author.username, 'alice')
        self.assertEqual(post.category.name, 'Technology')
        self.assertEqual(len(post.tags), 2)

    def test_create_post_unauthenticated_redirects(self):
        """Verify unauthenticated user cannot access /posts/new."""
        response = self.client.get('/posts/new')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/auth/login', response.location)

    def test_read_post_detail(self):
        """Verify viewing a single post via /posts/<id>."""
        post = Post(title='Detail Test', content='Content body here', user_id=self.author1.id)
        db.session.add(post)
        db.session.commit()

        response = self.client.get(f'/posts/{post.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Detail Test', response.data)
        self.assertIn(b'Content body here', response.data)

    def test_update_post_author_only(self):
        """Verify only the author can update their post."""
        post = Post(title='Original Title', content='Original Content', user_id=self.author1.id)
        db.session.add(post)
        db.session.commit()

        # Try to edit as Bob (not the author)
        self.login('bob')
        unauthorized_res = self.client.post(f'/posts/{post.id}/edit', data={
            'title': 'Hacked Title',
            'content': 'Hacked Content',
            'category_id': 0,
            'tags': ''
        }, follow_redirects=True)
        self.assertIn(b'not authorized to edit', unauthorized_res.data)

        # Title should NOT have changed
        refreshed_post = db.session.get(Post, post.id)
        self.assertEqual(refreshed_post.title, 'Original Title')

        # Now edit as Alice (the author)
        self.login('alice')
        authorized_res = self.client.post(f'/posts/{post.id}/edit', data={
            'title': 'Updated Title By Alice',
            'content': 'Updated Content',
            'category_id': 0,
            'tags': 'updated'
        }, follow_redirects=True)
        self.assertEqual(authorized_res.status_code, 200)

        # Verify DB update
        refreshed_post = db.session.get(Post, post.id)
        self.assertEqual(refreshed_post.title, 'Updated Title By Alice')

    def test_delete_post_author_only(self):
        """Verify only author can delete their post."""
        post = Post(title='To Be Deleted', content='Delete me', user_id=self.author1.id)
        db.session.add(post)
        db.session.commit()
        post_id = post.id

        # Try delete as Bob
        self.login('bob')
        unauth_del = self.client.post(f'/posts/{post_id}/delete', follow_redirects=True)
        self.assertIn(b'not authorized to delete', unauth_del.data)
        self.assertIsNotNone(db.session.get(Post, post_id))

        # Delete as Alice
        self.login('alice')
        auth_del = self.client.post(f'/posts/{post_id}/delete', follow_redirects=True)
        self.assertIn(b'has been deleted', auth_del.data)
        self.assertIsNone(db.session.get(Post, post_id))

    def test_category_and_tag_filtering(self):
        """Verify category and tag post listing views."""
        post = Post(title='Tagged Post', content='Content', user_id=self.author1.id, category_id=self.category.id)
        post.set_tags_from_string('dev')
        db.session.add(post)
        db.session.commit()

        # Category view
        cat_res = self.client.get(f'/posts/category/{self.category.slug}')
        self.assertEqual(cat_res.status_code, 200)
        self.assertIn(b'Tagged Post', cat_res.data)

        # Tag view
        tag_res = self.client.get('/posts/tag/dev')
        self.assertEqual(tag_res.status_code, 200)
        self.assertIn(b'Tagged Post', tag_res.data)


if __name__ == '__main__':
    unittest.main()
