import unittest
from app import app

class TestSecureDevApp(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_hello_endpoint(self):
        response = self.client.get('/hello?name=SecureDev')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello, SecureDev!', response.data)

if __name__ == '__main__':
    unittest.main()
