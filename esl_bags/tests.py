from rest_framework.test import APITestCase
from django.contrib.auth.hashers import make_password
import json
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

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
        user_request = {
            'email': 'test@mail.com',
            'first_name': 'test',
            'password': '1234'
        }

        response = self.client.post('/user/', user_request, format='json')
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data, {'email': 'test@mail.com', 'first_name': 'test'})


class TestUserLogin(APITestCase):
    def test_login_with_invalide_email(self):
        login_request = {
            'email': 'test',
            'password': 'test'
        }

        response = self.client.post('/user/login/', login_request, format='json')
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['non_field_errors'][0], 'Entre com um endereço de e-mail valido.')

    def test_login_without_email(self):
        login_request = {
            'email': '',
            'password': 'test'
        }

        response = self.client.post('/user/login/', login_request, format='json')
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['non_field_errors'][0], 'Entre com um endereço de e-mail valido.')

    def test_login_email_not_found(self):
        login_request = {
            'email': 'test@test.com',
            'password': 'test'
        }

        response = self.client.post('/user/login/', login_request, format='json')
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['non_field_errors'][0], 'E-mail não encontrado.')

    def test_login_password_wrong(self):
        User.objects.create(username="test@test.com", email="test@test.com", password="test")
        login_request = {
            'email': 'test@test.com',
            'password': 'wrong_password'
        }

        response = self.client.post('/user/login/', login_request, format='json')
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['non_field_errors'][0], 'E-mail ou senha incorretos.')

    def test_login_success(self):
        User.objects.create(username='test@test.com', email='test@test.com', first_name='test', password=make_password('test'))
        login_request = {
            'email': 'test@test.com',
            'password': 'test'
        }

        response = self.client.post('/user/login/', login_request, format='json')
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)


class TestGetUser(APITestCase):
    def test_get_user(self):
        user = User.objects.create(username='test@test.com', email='test@test.com', first_name='test', password=make_password('test'))
        token = Token.objects.create(user=user)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get('/user/')
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, {
                                "id": 1,
                                "email": "test@test.com",
                                "first_name": "test",
                                "is_staff": False,
                                "acquisitions": [],
                                "car": [],
                                "addresses": []
                        })


class TestUpdateUser(APITestCase):
        pass
