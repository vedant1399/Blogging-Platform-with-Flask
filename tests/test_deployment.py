import unittest
from app import create_app
from app.extensions import db
from config import ProductionConfig, DevelopmentConfig, TestingConfig


class DeploymentTestCase(unittest.TestCase):
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

    def test_production_config(self):
        """Verify production configuration flags."""
        self.assertFalse(ProductionConfig.DEBUG)
        self.assertFalse(hasattr(ProductionConfig, 'TESTING') and ProductionConfig.TESTING)

    def test_wsgi_entrypoint_import(self):
        """Verify wsgi.py loads a valid Flask application callable."""
        import wsgi
        self.assertIsNotNone(wsgi.app)
        self.assertTrue(hasattr(wsgi.app, 'wsgi_app'))

    def test_health_check_endpoint(self):
        """Verify health check endpoint for container/orchestrator probes."""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'healthy')
        self.assertTrue(data.get('auth_enabled'))

    def test_custom_404_error_handler(self):
        """Verify custom 404 error page renders properly."""
        response = self.client.get('/this-route-definitely-does-not-exist-404')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Page Not Found', response.data)
        self.assertIn(b'404', response.data)

    def test_security_headers_and_status(self):
        """Verify home page loads properly without error."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
