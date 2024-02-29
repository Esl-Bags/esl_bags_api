from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from products.models import Brand
from django.contrib.auth.hashers import make_password
import json

# Create your tests here.
class TestBrandCreate(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test@test.com', email='test@test.com', first_name='test', password=make_password('test'))

    def test_create_brand(self):
        self.user.is_staff = True
        self.user.save()
        self.client.force_authenticate(self.user)

        brand_request = {
            'name': 'test'
        }

        response = self.client.post('/product/brand/', brand_request, format='json')
        data = json.loads(response.content)

        self.assertEqual(data, { 'name': 'test' })

    def test_create_brand_without_permission(self):
        self.client.force_authenticate(self.user)

        brand_request = {
            'name': 'test'
        }

        response = self.client.post('/product/brand/', brand_request, format='json')
        data = json.loads(response.content)

        self.assertEqual(data, { 'detail': 'Usuário não tem permissão para cadastro de marcas.' })


    def test_create_brand_already_registered(self):
        self.user.is_staff = True
        self.user.save()
        self.client.force_authenticate(self.user)

        Brand.objects.create(name='test')
        brand_request = {
            'name': 'test'
        }

        response = self.client.post('/product/brand/', brand_request, format='json')
        data = json.loads(response.content)

        self.assertEqual(data['name'][0], 'A marca já foi registrada.')

    def test_create_brand_with_name_too_short(self):
        self.user.is_staff = True
        self.user.save()
        self.client.force_authenticate(self.user)

        brand_request = {
            'name': 'te'
        }

        response = self.client.post('/product/brand/', brand_request, format='json')
        data = json.loads(response.content)

        self.assertEqual(data['name'][0], 'A marca deve conter mais de dois caracteres.')


class TestListBrand(APITestCase):
    def test_list_brand(self):
        Brand.objects.create(name='test')
        
        response = self.client.get('/product/brand/')
        data = json.loads(response.content)

        self.assertEqual(data, [{'name': 'test'}])