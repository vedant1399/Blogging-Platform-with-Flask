import unittest
from app import create_app
from app.extensions import db
from app.models import User, Post, Category, Tag


class FrontendPaginationTestCase(unittest.TestCase):
    def setUp(self):
        """Set up testing app and in-memory test database."""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

        # Create author
        self.author = User(username='janedoe', email='jane@example.com')
        self.author.set_password('password123')
        db.session.add(self.author)

        # Create category
        self.category = Category(name='Frontend', description='UI and templates')
        db.session.add(self.category)
        db.session.commit()

        # Seed 9 posts to test multi-page pagination
        for i in range(1, 10):
            p = Post(
                title=f'Article Number {i}',
                content=f'<p>This is paragraph content for article {i}. It tests Jinja2 rendering and pagination.</p>',
                user_id=self.author.id,
                category_id=self.category.id
            )
            p.set_tags_from_string('frontend, jinja2')
            db.session.add(p)
        db.session.commit()

    def tearDown(self):
        """Tear down database and application context."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page_pagination(self):
        """Verify home page pagination across multiple pages."""
        # Page 1 (per_page=4, so 4 posts)
        res_p1 = self.client.get('/')
        self.assertEqual(res_p1.status_code, 200)
        self.assertIn(b'Article Number 9', res_p1.data)
        self.assertIn(b'Article Number 8', res_p1.data)
        self.assertIn(b'Article Number 7', res_p1.data)
        self.assertIn(b'Article Number 6', res_p1.data)
        # Should contain pagination navigation
        self.assertIn(b'Showing page', res_p1.data)
        self.assertIn(b'Next', res_p1.data)

        # Page 2
        res_p2 = self.client.get('/?page=2')
        self.assertEqual(res_p2.status_code, 200)
        self.assertIn(b'Article Number 5', res_p2.data)
        self.assertIn(b'Previous', res_p2.data)

        # Page 3 (final post)
        res_p3 = self.client.get('/?page=3')
        self.assertEqual(res_p3.status_code, 200)
        self.assertIn(b'Article Number 1', res_p3.data)

    def test_post_detail_view_and_navigation(self):
        """Verify individual post template with breadcrumbs and prev/next links."""
        target_post = Post.query.filter_by(title='Article Number 5').first()
        res = self.client.get(f'/posts/{target_post.id}')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Article Number 5', res.data)
        self.assertIn(b'janedoe', res.data)
        self.assertIn(b'Frontend', res.data)
        self.assertIn(b'min read', res.data)
        # Next / Previous navigation presence
        self.assertIn(b'Previous Article', res.data)
        self.assertIn(b'Next Article', res.data)

    def test_author_public_profile_pagination(self):
        """Verify author profile page and its paginated post list."""
        # Profile page 1
        res = self.client.get('/users/janedoe')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'janedoe', res.data)
        self.assertIn(b'jane@example.com', res.data)
        self.assertIn(b'Articles by janedoe', res.data)
        self.assertIn(b'9 published articles', res.data)

        # Profile page 2
        res_p2 = self.client.get('/users/janedoe?page=2')
        self.assertEqual(res_p2.status_code, 200)
        self.assertIn(b'Showing page', res_p2.data)

        # Non-existent user returns 404
        res_404 = self.client.get('/users/nonexistentuser')
        self.assertEqual(res_404.status_code, 404)

    def test_jinja2_custom_filters(self):
        """Verify custom reading_time and format_datetime filters."""
        with self.app.test_request_context():
            reading_time_filter = self.app.jinja_env.filters['reading_time']
            format_datetime_filter = self.app.jinja_env.filters['format_datetime']

            # Short text
            self.assertEqual(reading_time_filter('<p>Hello world this is a test</p>'), '1 min read')

            # Long text (400 words)
            long_text = ' '.join(['word'] * 400)
            self.assertEqual(reading_time_filter(f'<p>{long_text}</p>'), '2 min read')

            # None handling
            self.assertEqual(format_datetime_filter(None), '')


if __name__ == '__main__':
    unittest.main()
