import unittest
from app import create_app
from app.extensions import db
from app.models import User, Post, Category, Comment


class CommentsTestCase(unittest.TestCase):
    def setUp(self):
        """Set up testing app and in-memory test database."""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

        # Users: Post Author, Commenter, and Stranger
        self.author = User(username='author_user', email='author@example.com')
        self.author.set_password('password123')

        self.commenter = User(username='commenter_user', email='commenter@example.com')
        self.commenter.set_password('password123')

        self.stranger = User(username='stranger_user', email='stranger@example.com')
        self.stranger.set_password('password123')

        db.session.add_all([self.author, self.commenter, self.stranger])
        db.session.commit()

        # Create a post
        self.post = Post(
            title='Post to be Commented',
            content='This is a discussion post for testing comments.',
            user_id=self.author.id
        )
        db.session.add(self.post)
        db.session.commit()

    def tearDown(self):
        """Tear down database and application context."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login(self, username, password='password123'):
        """Helper to log in a user."""
        self.client.get('/auth/logout')
        return self.client.post('/auth/login', data={
            'identifier': username,
            'password': password
        }, follow_redirects=True)

    def test_comment_model_and_relations(self):
        """Verify Comment model relationships with User and Post."""
        comment = Comment(
            content='Great article! Thanks for sharing.',
            user_id=self.commenter.id,
            post_id=self.post.id
        )
        db.session.add(comment)
        db.session.commit()

        # Verify post.comments relation
        self.assertEqual(self.post.comments.count(), 1)
        self.assertEqual(self.post.comments.first().content, 'Great article! Thanks for sharing.')
        self.assertEqual(self.post.comments.first().author.username, 'commenter_user')

        # Verify user.comments relation
        self.assertEqual(self.commenter.comments.count(), 1)
        self.assertEqual(self.commenter.comments.first().post.title, 'Post to be Commented')

    def test_add_comment_authenticated(self):
        """Verify authenticated user can post a comment."""
        self.login('commenter_user')
        response = self.client.post(f'/posts/{self.post.id}/comments', data={
            'content': 'I really enjoyed this post!'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your comment has been posted!', response.data)
        self.assertIn(b'I really enjoyed this post!', response.data)

        # Check in DB
        comment = Comment.query.filter_by(post_id=self.post.id).first()
        self.assertIsNotNone(comment)
        self.assertEqual(comment.author.username, 'commenter_user')

    def test_add_comment_unauthenticated_redirects(self):
        """Verify unauthenticated user cannot post a comment."""
        response = self.client.post(f'/posts/{self.post.id}/comments', data={
            'content': 'Anonymous comment attempt'
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn('/auth/login', response.location)
        self.assertEqual(Comment.query.count(), 0)

    def test_add_comment_empty_validation(self):
        """Verify empty comment submission fails validation."""
        self.login('commenter_user')
        response = self.client.post(f'/posts/{self.post.id}/comments', data={
            'content': '   '
        }, follow_redirects=True)

        self.assertIn(b'Comment cannot be empty', response.data)
        self.assertEqual(Comment.query.count(), 0)

    def test_comment_deletion_by_comment_author(self):
        """Verify comment author can delete their own comment."""
        comment = Comment(content='My temporary comment', user_id=self.commenter.id, post_id=self.post.id)
        db.session.add(comment)
        db.session.commit()
        comment_id = comment.id

        self.login('commenter_user')
        res = self.client.post(f'/posts/comments/{comment_id}/delete', follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Comment deleted.', res.data)
        self.assertIsNone(db.session.get(Comment, comment_id))

    def test_comment_deletion_by_post_author(self):
        """Verify post author can moderate/delete comments on their post."""
        comment = Comment(content='Inappropriate comment', user_id=self.commenter.id, post_id=self.post.id)
        db.session.add(comment)
        db.session.commit()
        comment_id = comment.id

        # Post author logs in and deletes
        self.login('author_user')
        res = self.client.post(f'/posts/comments/{comment_id}/delete', follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Comment deleted.', res.data)
        self.assertIsNone(db.session.get(Comment, comment_id))

    def test_comment_deletion_forbidden_for_stranger(self):
        """Verify random third party cannot delete someone else's comment."""
        comment = Comment(content='Legit comment', user_id=self.commenter.id, post_id=self.post.id)
        db.session.add(comment)
        db.session.commit()
        comment_id = comment.id

        # Stranger attempts delete
        self.login('stranger_user')
        res = self.client.post(f'/posts/comments/{comment_id}/delete', follow_redirects=True)
        self.assertIn(b'not authorized to delete this comment', res.data)
        self.assertIsNotNone(db.session.get(Comment, comment_id))

    def test_cascade_delete_comments_with_post(self):
        """Verify deleting a post automatically deletes all its comments."""
        c1 = Comment(content='Comment 1', user_id=self.commenter.id, post_id=self.post.id)
        c2 = Comment(content='Comment 2', user_id=self.stranger.id, post_id=self.post.id)
        db.session.add_all([c1, c2])
        db.session.commit()
        self.assertEqual(Comment.query.count(), 2)

        # Delete post
        self.login('author_user')
        self.client.post(f'/posts/{self.post.id}/delete', follow_redirects=True)

        # Comments should be cascaded and deleted
        self.assertEqual(Comment.query.count(), 0)


if __name__ == '__main__':
    unittest.main()
