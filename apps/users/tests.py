from django.test import TestCase, Client
from rest_framework.authtoken.models import Token

from apps.users.models import CustomUser


class UserTests(TestCase):
    def setUp(self):
        # Initialize Client
        self.client = Client()
        # Create two users
        n = CustomUser.objects.create(username='normal_u', role='normal')
        a = CustomUser.objects.create(username='admin_u', role='admin')
        n.set_password('password1234')
        n.save()
        a.set_password('password1234')
        a.save()

    def test_user_created(self):
        """
        Test creation of users in database
        """
        normal = CustomUser.objects.get(role='normal')
        admin = CustomUser.objects.get(role='admin')
        assert normal.username == 'normal_u'
        assert admin.username == 'admin_u'

    def test_signup(self):
        """
        Test signup endpoint
        """
        response = self.client.post(path='/api/v1/auth/signup/',
                                    data={'username': 'test_u', 'password': 'password1234'})
        assert response.status_code == 201

    def test_login(self):
        """
        Test login endpoint
        """
        response = self.client.post(path='/api/v1/auth/login/',
                                    data={'username': 'normal_u', 'password': 'password1234'})
        token_in_db = Token.objects.get(user=CustomUser.objects.get(username='normal_u'))
        assert response.status_code == 200
        assert 'token' in response.data.keys()
        assert response.data['token'] == token_in_db.key
