from rest_framework.test import APITestCase
import json
from django.contrib.auth.models import User

class TestCreateUser(APITestCase):
    def test_create_user_without_email(self):
        user_request = {
            'email': '',
            'first_name': 'test',
            'password': 'test'
        }

        response = self.client.post('/user/', user_request, format='json')
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['email'][0], 'O e-mail é obrigatorio.')

    def test_create_user_with_invalide_email(self):
        user_request = {
            'email': 'test',
            'first_name': 'test',
            'password': 'test'
        }

        response = self.client.post('/user/', user_request, format='json')
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['email'][0], 'Entre com um endereço de e-mail valido.')

    def test_create_user_with_email_in_use(self):
        User.objects.create(username='test@mail.com', email='test@mail.com', password='test')
        user_request = {
            'email': 'test@mail.com',
            'first_name': 'test',
            'password': 'test'
        }

        response = self.client.post('/user/', user_request, format='json')
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['email'][0], 'O e-mail já é usado.')


    def test_create_user_without_name(self):
        user_request = {
            'email': 'test@mail.com',
            'first_name': '',
            'password': 'test'
        }

        response = self.client.post('/user/', user_request, format='json')
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['first_name'][0], 'O nome é obrigatorio.')

    def test_create_user_with_name_short(self):
        user_request = {
            'email': 'test@mail.com',
            'first_name': 'abc',
            'password': 'test'
        }

        response = self.client.post('/user/', user_request, format='json')
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['first_name'][0], 'O nome deve conter pelo menos 4 caracteres.')

    def test_create_user_without_password(self):
        user_request = {
            'email': 'test@mail.com',
            'first_name': 'test',
            'password': ''
        }

        response = self.client.post('/user/', user_request, format='json')
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['password'][0], 'A senha é obrigatoria.')

    def test_create_user_with_password_short(self):
        user_request = {
            'email': 'test@mail.com',
            'first_name': 'test',
            'password': '123'
        }

        response = self.client.post('/user/', user_request, format='json')
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['password'][0], 'A senha deve conter pelo menos 4 caracteres.')

    def test_create_user(self):
        pass
