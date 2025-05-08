import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from routes import BlacklistResource, api_bp

# Define tu token estático
AUTH_TOKEN = "mi_token_predefinido"

@patch('routes.token_required', lambda f: f)
class TestAPI(unittest.TestCase):

    def setUp(self):
        from routes import BlacklistResource  # Importar aquí para que respete el patch
        self.app = Flask(__name__)
        self.app.register_blueprint(api_bp)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()


    def test_health_check(self):
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 404)
        
        self.assertEqual(response.get_json(), {"status": "OK"})

    @patch('routes.db.session.add')
    @patch('routes.db.session.commit')
    @patch('routes.Blacklist')
    def test_post_blacklist_success(self, mock_blacklist, mock_commit, mock_add):
        mock_instance = MagicMock()
        mock_instance.to_dict.return_value = {
            "email": "test@example.com",
            "app_uuid": "123",
            "blocked_reason": "spam",
            "ip_address": "127.0.0.1"
        }
        mock_blacklist.return_value = mock_instance

        response = self.client.post(
            '/blacklists',
            json={
                "email": "test@example.com",
                "app_uuid": "123",
                "blocked_reason": "spam"
            },
            headers={
                "X-Forwarded-For": "127.0.0.1",
                "Authorization": f"Bearer {AUTH_TOKEN}"  # Agregar el token estático en los headers
            }
        )

        self.assertEqual(response.status_code, 201)
        self.assertIn("Email added to blacklist", response.get_json()["message"])

    def test_post_blacklist_missing_fields(self):
        response = self.client.post('/blacklists', json={}, headers={"Authorization": f"Bearer {AUTH_TOKEN}"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()["message"], "Email and app_uuid are required")

    @patch('routes.Blacklist.query')
    def test_get_blacklist_found(self, mock_query):
        mock_entry = MagicMock()
        mock_entry.blocked_reason = "spam"
        mock_query.filter_by.return_value.first.return_value = mock_entry

        response = self.client.get(
            '/blacklists/test@example.com',
            headers={"Authorization": f"Bearer {AUTH_TOKEN}"}  # Incluir token en los headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.get_json()["blacklisted"])
        self.assertEqual(response.get_json()["reason"], "spam")

    @patch('routes.Blacklist.query')
    def test_get_blacklist_not_found(self, mock_query):
        mock_query.filter_by.return_value.first.return_value = None

        response = self.client.get(
            '/blacklists/test@example.com',
            headers={"Authorization": f"Bearer {AUTH_TOKEN}"}  # Incluir token en los headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.get_json()["blacklisted"])

if __name__ == '__main__':
    unittest.main()