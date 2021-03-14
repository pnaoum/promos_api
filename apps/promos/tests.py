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
        n = CustomUser.objects.create(username='normal_u', role='normal')
        a = CustomUser.objects.create(username='admin_u', role='admin')
        normal_token = Token.objects.create(user=n).key
        admin_token = Token.objects.create(user=a).key
        self.normal_auth_header = {'HTTP_AUTHORIZATION': 'Token ' + normal_token}
        self.admin_auth_header = {'HTTP_AUTHORIZATION': 'Token ' + admin_token}

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
        response = self.client.get(path='/api/v1/users/me/promos/code/')
        assert response.status_code == 401
        response = self.client.post(path='/api/v1/users/me/promos/code/')
        assert response.status_code == 401
        response = self.client.get(path='/api/v1/users/1/promos/')
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
        response = self.client.get(path='/api/v1/users/1/promos/', **self.normal_auth_header)
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
                                    data={'promo_code': 'PROMO1', 'amount': 100, 'start_time': datetime.now(tz=UTC),
                                          'type': 'discount', 'is_active': True, 'description': 'Test Promo'})
        assert response.status_code == 201
        assert Promo.objects.count() == 1

    def test_edit_promo(self):
        """
        Edit Promo
        """
        Promo.objects.create(**{'promo_code': 'PROMO1', 'amount': 100, 'start_time': datetime.now(tz=UTC),
                                'type': 'discount', 'is_active': True, 'description': 'Test Promo'})
        response = self.client.put(path='/api/v1/promos/PROMO1/', **self.admin_auth_header,
                                   data={'promo_code': 'PROMO2', 'amount': 100, 'start_time': datetime.now(tz=UTC),
                                         'type': 'discount', 'is_active': True, 'description': 'Test Promo'},
                                   content_type='application/json')
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
        Promo.objects.create(**{'promo_code': 'PROMO1', 'amount': 100, 'start_time': datetime.now(tz=UTC),
                                'type': 'discount', 'is_active': True, 'description': 'Test Promo'})
        # Assert created
        assert Promo.objects.count() == 1
        response = self.client.delete(path='/api/v1/promos/PROMO1/', **self.admin_auth_header)
        assert response.status_code == 204
        # Assert deleted
        assert Promo.objects.count() == 0

    def test_assign_promo(self):
        """
        Assign Promo to user
        """
        Promo.objects.create(**{'promo_code': 'PROMO1', 'amount': 100, 'start_time': datetime.now(tz=UTC),
                                'type': 'discount', 'is_active': True, 'description': 'Test Promo'})
        n = CustomUser.objects.get(username='normal_u')
        response = self.client.post(path='/api/v1/users/' + str(n.id) + '/promos/', data={'promo_code': 'PROMO1'},
                                    **self.admin_auth_header)
        assert response.status_code == 201
        # Assert from user api
        response = self.client.get(path='/api/v1/users/me/promos/', **self.normal_auth_header)
        assert response.status_code == 200
        assert len(response.data['results']) > 0

    def test_consume_points(self):
        """
        Consume Points
        """
        Promo.objects.create(**{'promo_code': 'PROMO1', 'amount': 100, 'start_time': datetime.now(tz=UTC),
                                'type': 'discount', 'is_active': True, 'description': 'Test Promo'})
        n = CustomUser.objects.get(username='normal_u')
        response = self.client.post(path='/api/v1/users/' + str(n.id) + '/promos/', data={'promo_code': 'PROMO1'},
                                    **self.admin_auth_header)
        assert response.status_code == 201
        # Consume points
        response = self.client.post(path='/api/v1/users/me/promos/PROMO1/', data={'points': 20},
                                    **self.normal_auth_header)
        assert response.status_code == 202
        assert response.data['points'] == 80
        # Retrieve points
        response = self.client.get(path='/api/v1/users/me/promos/PROMO1/', **self.normal_auth_header)
        assert response.data['points'] == 80
