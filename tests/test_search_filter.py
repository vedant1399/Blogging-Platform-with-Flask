import unittest
from app import create_app
from app.extensions import db
from app.models import User, Post, Category, Tag, Comment


class SearchAndFilterTestCase(unittest.TestCase):
    def setUp(self):
        """Set up testing app and in-memory test database."""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

        # Create user
        self.author = User(username='searchdev', email='searchdev@example.com')
        self.author.set_password('password123')
        db.session.add(self.author)

        # Create categories
        self.cat_python = Category(name='Python', description='Python guides')
        self.cat_devops = Category(name='DevOps', description='DevOps and Cloud')
        db.session.add_all([self.cat_python, self.cat_devops])
        db.session.commit()

        # Create sample posts
        self.post1 = Post(
            title='Mastering Flask Web Development',
            content='Flask is a lightweight WSGI web framework in Python.',
            user_id=self.author.id,
            category_id=self.cat_python.id
        )
        self.post1.set_tags_from_string('flask, python, backend')

        self.post2 = Post(
            title='Dockerizing Your Applications',
            content='Containerize microservices using Docker containers and Docker Compose.',
            user_id=self.author.id,
            category_id=self.cat_devops.id
        )
        self.post2.set_tags_from_string('docker, devops, containers')

        self.post3 = Post(
            title='Advanced SQLAlchemy Queries',
            content='Learn about joins, filters, subqueries, and database indexing in Python with SQLAlchemy.',
            user_id=self.author.id,
            category_id=self.cat_python.id
        )
        self.post3.set_tags_from_string('database, sqlalchemy, python')

        db.session.add_all([self.post1, self.post2, self.post3])
        db.session.commit()

        # Add comments to post3 so it is the most popular
        c1 = Comment(content='Great SQLAlchemy tips!', user_id=self.author.id, post_id=self.post3.id)
        c2 = Comment(content='Helped me optimize queries.', user_id=self.author.id, post_id=self.post3.id)
        db.session.add_all([c1, c2])
        db.session.commit()

    def tearDown(self):
        """Tear down database and application context."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_search_by_title(self):
        """Verify searching posts by title keyword."""
        response = self.client.get('/posts/?q=Dockerizing')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dockerizing Your Applications', response.data)
        self.assertNotIn(b'Mastering Flask', response.data)
        self.assertNotIn(b'Advanced SQLAlchemy', response.data)

    def test_search_by_content(self):
        """Verify searching posts by content body."""
        response = self.client.get('/posts/?q=lightweight')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Mastering Flask Web Development', response.data)
        self.assertNotIn(b'Dockerizing Your Applications', response.data)

    def test_search_case_insensitivity(self):
        """Verify search is case-insensitive (ILIKE)."""
        response = self.client.get('/posts/?q=FLASK')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Mastering Flask Web Development', response.data)

    def test_filter_by_category(self):
        """Verify filtering posts by category slug."""
        response = self.client.get(f'/posts/?category={self.cat_devops.slug}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dockerizing Your Applications', response.data)
        self.assertNotIn(b'Mastering Flask', response.data)
        self.assertNotIn(b'Advanced SQLAlchemy', response.data)

    def test_filter_by_tag(self):
        """Verify filtering posts by tag slug."""
        tag = Tag.query.filter_by(name='backend').first()
        response = self.client.get(f'/posts/?tag={tag.slug}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Mastering Flask Web Development', response.data)
        self.assertNotIn(b'Dockerizing Your Applications', response.data)

    def test_combined_search_and_category_filter(self):
        """Verify combining keyword search and category filter."""
        # Searching "Python" in "Python" category should return post1 and post3
        res = self.client.get(f'/posts/?q=Python&category={self.cat_python.slug}')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Mastering Flask Web Development', res.data)
        self.assertIn(b'Advanced SQLAlchemy Queries', res.data)
        self.assertNotIn(b'Dockerizing Your Applications', res.data)

        # Searching "Docker" inside "Python" category should yield 0 results
        res_empty = self.client.get(f'/posts/?q=Docker&category={self.cat_python.slug}')
        self.assertEqual(res_empty.status_code, 200)
        self.assertIn(b'No matching articles found', res_empty.data)

    def test_sort_by_popularity_most_commented(self):
        """Verify sorting by popularity (most commented posts first)."""
        res = self.client.get('/posts/?sort=popular')
        self.assertEqual(res.status_code, 200)
        # post3 has 2 comments, post1 and post2 have 0
        data = res.get_data(as_text=True)
        idx_post3 = data.find('Advanced SQLAlchemy Queries')
        idx_post1 = data.find('Mastering Flask Web Development')
        self.assertTrue(idx_post3 < idx_post1, "Post with more comments should appear first in popular sort")

    def test_search_redirect_route(self):
        """Verify /posts/search redirects with query parameter to /posts/."""
        res = self.client.get('/posts/search?q=testquery')
        self.assertEqual(res.status_code, 302)
        self.assertIn('q=testquery', res.location)


if __name__ == '__main__':
    unittest.main()
