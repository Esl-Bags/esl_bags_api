from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from products.models import Brand, Product
from django.contrib.auth.hashers import make_password
import json

from PIL import Image
import tempfile

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

        self.assertEqual(data, { 'id': 1,'name': 'test' })

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

        self.assertEqual(data, [{'id': 1, 'name': 'test'}])


class TestRetriveBrand(APITestCase):
    def test_retrive_brand(self):
        Brand.objects.create(name='test')
        
        response = self.client.get('/product/brand/1/')
        data = json.loads(response.content)

        self.assertEqual(data, {'id': 1, 'name': 'test'})


class TestUpdateBrand(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test@test.com', email='test@test.com', first_name='test', password=make_password('test'))
        
    def test_update_brand(self):
        self.user.is_staff = True
        self.user.save()
        self.client.force_authenticate(self.user)
        Brand.objects.create(name='test')
        request_change = { 'name': 'test_change' }
        
        response = self.client.patch('/product/brand/1/', request_change, format='json')
        data = json.loads(response.content)

        self.assertEqual(data, {'id': 1, 'name': 'test_change'})


class TestProductCreate(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test@test.com', email='test@test.com', first_name='test', password=make_password('test'))

    def test_create_product(self):
        self.user.is_staff = True
        self.user.save()
        self.client.force_authenticate(self.user)

        image = Image.new('RGB', (100, 100))

        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        tmp_file.seek(0)

        brand = Brand.objects.create(name="test")

        product_request = {
            'name': 'test',
            'photo': tmp_file,
            'description': 'test',
            'price': '50',
            'brand': brand.name
        }

        response = self.client.post('/product/', product_request, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestListProduct(APITestCase):
    def test_list_product(self):        
        response = self.client.get('/product/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestRetriveProduct(APITestCase):
    def test_retrive_product(self):
        brand = Brand.objects.create(name='test')

        Product.objects.create(name='test', description='test', price=50, brand=brand)
        
        response = self.client.get('/product/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
