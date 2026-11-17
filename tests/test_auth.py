import unittest
from app import create_app
from app.extensions import db
from app.models import User, Post

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        """Set up testing application and clean database."""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        """Tear down database and application context."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        """Verify that passwords are securely hashed and checked."""
        u = User(username='testauth', email='auth@example.com')
        u.set_password('mysecretpassword')
        self.assertTrue(u.password_hash is not None)
        self.assertNotEqual(u.password_hash, 'mysecretpassword')
        self.assertTrue(u.check_password('mysecretpassword'))
        self.assertFalse(u.check_password('wrongpassword'))

    def test_registration_success(self):
        """Verify successful user registration via auth blueprint."""
        response = self.client.post('/auth/register', data={
            'username': 'newauthor',
            'email': 'newauthor@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Registration successful', response.data)

        # Check user in database
        user = User.query.filter_by(username='newauthor').first()
        self.assertIsNotNone(user)
        self.assertTrue(user.check_password('password123'))

    def test_registration_validation(self):
        """Verify registration validations (password mismatch, duplicate username)."""
        # Create existing user
        u = User(username='existing', email='existing@example.com')
        u.set_password('pass123')
        db.session.add(u)
        db.session.commit()

        # Try duplicate username
        res_dup = self.client.post('/auth/register', data={
            'username': 'existing',
            'email': 'different@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }, follow_redirects=True)
        self.assertIn(b'Username is already taken', res_dup.data)

        # Try password mismatch
        res_mismatch = self.client.post('/auth/register', data={
            'username': 'brandnew',
            'email': 'brandnew@example.com',
            'password': 'passwordA',
            'confirm_password': 'passwordB'
        }, follow_redirects=True)
        self.assertIn(b'Passwords do not match', res_mismatch.data)

    def test_login_and_logout(self):
        """Verify login, session management, and logout."""
        # Create user
        user = User(username='blogger', email='blogger@example.com')
        user.set_password('securepass123')
        db.session.add(user)
        db.session.commit()

        # Login with correct password
        login_res = self.client.post('/auth/login', data={
            'identifier': 'blogger',
            'password': 'securepass123'
        }, follow_redirects=True)
        self.assertEqual(login_res.status_code, 200)
        self.assertIn(b'Welcome back, blogger!', login_res.data)

        # Access protected profile page
        profile_res = self.client.get('/auth/profile')
        self.assertEqual(profile_res.status_code, 200)
        self.assertIn(b'Authenticated Session', profile_res.data)

        # Logout
        logout_res = self.client.get('/auth/logout', follow_redirects=True)
        self.assertEqual(logout_res.status_code, 200)
        self.assertIn(b'logged out successfully', logout_res.data)

        # Profile should now redirect to login
        profile_after_logout = self.client.get('/auth/profile')
        self.assertEqual(profile_after_logout.status_code, 302)
        self.assertIn('/auth/login', profile_after_logout.location)

    def test_login_invalid_credentials(self):
        """Verify login failure with incorrect credentials."""
        user = User(username='blogger2', email='blogger2@example.com')
        user.set_password('correctpass')
        db.session.add(user)
        db.session.commit()

        res = self.client.post('/auth/login', data={
            'identifier': 'blogger2',
            'password': 'wrongpassword'
        }, follow_redirects=True)
        self.assertIn(b'Invalid username/email or password', res.data)

    def test_protected_routes_require_login(self):
        """Verify that @login_required protects routes from unauthenticated users."""
        res = self.client.get('/auth/profile')
        self.assertEqual(res.status_code, 302)
        self.assertIn('/auth/login', res.location)

        post_res = self.client.post('/create-post', data={
            'title': 'Unauthorized Post',
            'content': 'Should not work'
        })
        self.assertEqual(post_res.status_code, 302)
        self.assertIn('/auth/login', post_res.location)


if __name__ == '__main__':
    unittest.main()
