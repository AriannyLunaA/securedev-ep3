import unittest
from app import app


class TestSecureDevApp(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_hello_endpoint(self):
        response = self.client.get("/hello?name=SecureDev")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Hello, SecureDev!", response.data)

    def test_xss_mitigation(self):
        response = self.client.get("/hello?name=<script>alert(1)</script>")
        self.assertEqual(response.status_code, 400)
        self.assertNotIn(b"<script>", response.data)

    def test_security_headers(self):
        response = self.client.get("/hello?name=SecureDev")
        self.assertIn("Content-Security-Policy", response.headers)
        self.assertEqual(response.headers.get("X-Frame-Options"), "DENY")
        self.assertEqual(response.headers.get("X-Content-Type-Options"), "nosniff")
        self.assertIn("Permissions-Policy", response.headers)


if __name__ == "__main__":
    unittest.main()
