from django.test import TestCase, Client


class HealthTests(TestCase):
    def setUp(self):
        # Initialize Client
        self.client = Client()

    def test_health(self):
        """
        Test Health of the App
        """
        response = self.client.get(path='/api/v1/health/')
        assert response.status_code == 200
