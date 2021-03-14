from datetime import datetime

from django.test import TestCase, Client
from pytz import UTC
from rest_framework.authtoken.models import Token

from apps.promos.models import Promo
from apps.users.models import CustomUser


class PromoTests(TestCase):
    def setUp(self):
        # Initialize Client
        self.client = Client()
        # Create two users and save tokens
        self.normal_user = CustomUser.objects.create(username='normal_u', role='normal')
        self.admin_user = CustomUser.objects.create(username='admin_u', role='admin')
        normal_token = Token.objects.create(user=self.normal_user).key
        admin_token = Token.objects.create(user=self.admin_user).key
        self.normal_auth_header = {'HTTP_AUTHORIZATION': 'Token ' + normal_token}
        self.admin_auth_header = {'HTTP_AUTHORIZATION': 'Token ' + admin_token}

        self.promo_dict = {'promo_code': 'PROMO1', 'points': 100, 'start_time': datetime.now(tz=UTC),
                           'type': 'discount', 'is_active': True, 'description': 'Test Promo',
                           'user': self.normal_user}
        self.promo_request = {'promo_code': 'PROMO1', 'points': 100, 'start_time': datetime.now(tz=UTC),
                              'type': 'discount', 'is_active': True, 'description': 'Test Promo',
                              'user': self.normal_user.id}

    # Authentication
    def test_auth(self):
        """
        Test endpoints usage without token
        """
        response = self.client.get(path='/api/v1/promos/')
        assert response.status_code == 401
        response = self.client.post(path='/api/v1/promos/')
        assert response.status_code == 401
        response = self.client.put(path='/api/v1/promos/code/')
        assert response.status_code == 401
        response = self.client.delete(path='/api/v1/promos/code/')
        assert response.status_code == 401
        response = self.client.get(path='/api/v1/users/me/promos/')
        assert response.status_code == 401
        response = self.client.get(path='/api/v1/users/me/promos/code/points/')
        assert response.status_code == 401
        response = self.client.put(path='/api/v1/users/me/promos/code/points/')
        assert response.status_code == 401

    # Access
    def test_non_admin_access(self):
        """
        Test endpoints that are only allowed to admins by normal users
        """
        response = self.client.get(path='/api/v1/promos/', **self.normal_auth_header)
        assert response.status_code == 403
        response = self.client.post(path='/api/v1/promos/', **self.normal_auth_header)
        assert response.status_code == 403
        response = self.client.put(path='/api/v1/promos/code/', **self.normal_auth_header)
        assert response.status_code == 403
        response = self.client.delete(path='/api/v1/promos/code/', **self.normal_auth_header)
        assert response.status_code == 403

    def test_admin_access(self):
        """
        Test endpoints that are only allowed to admins by admin users
        """
        response = self.client.get(path='/api/v1/promos/', **self.admin_auth_header)
        assert response.status_code == 200

    # Promo
    def test_create_promo(self):
        """
        Create Promo
        """
        response = self.client.post(path='/api/v1/promos/', **self.admin_auth_header,
                                    data=self.promo_request)
        assert response.status_code == 201
        assert Promo.objects.count() == 1

    def test_edit_promo(self):
        """
        Edit Promo
        """
        Promo.objects.create(**self.promo_dict)
        new_promo = self.promo_request
        new_promo['promo_code'] = 'PROMO2'
        response = self.client.put(path='/api/v1/promos/PROMO1/', **self.admin_auth_header,
                                   data=new_promo, content_type='application/json')
        assert response.status_code == 200
        # Assert name changed
        response = self.client.get(path='/api/v1/promos/?promo_code=PROMO2', **self.admin_auth_header)
        assert len(response.data['results']) > 0
        response = self.client.get(path='/api/v1/promos/?promo_code=PROMO1', **self.admin_auth_header)
        assert len(response.data['results']) == 0

    def test_delete_promo(self):
        """
        Delete Promo
        """
        Promo.objects.create(**self.promo_dict)
        # Assert created
        assert Promo.objects.count() == 1
        response = self.client.delete(path='/api/v1/promos/PROMO1/', **self.admin_auth_header)
        assert response.status_code == 204
        # Assert deleted
        assert Promo.objects.count() == 0

    def test_consume_points(self):
        """
        Consume Points
        """
        Promo.objects.create(**self.promo_dict)
        # Consume points
        response = self.client.put(path='/api/v1/users/me/promos/PROMO1/points/', data={'points': 20},
                                   **self.normal_auth_header, content_type='application/json')
        assert response.status_code == 202
        assert response.data['points'] == 80
        # Retrieve points
        response = self.client.get(path='/api/v1/users/me/promos/PROMO1/points/', **self.normal_auth_header)
        assert response.data['points'] == 80
