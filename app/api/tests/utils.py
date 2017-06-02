from base64 import b64encode

from django.contrib.auth.models import User


admin_test_credentials = ('admin1', 'admin@taverna.com', 'qwerty123',)
normal_user_credentials = ('user1', 'user1@taverna.com', 'qwerty123',)
endpoint = '/api'


def obtain_api_key(client):
        credentials = '{}:{}'.format(
            admin_test_credentials[0],
            admin_test_credentials[2]
        )
        b64_encoded_credentials = b64encode(credentials.encode('utf-8'))
        return client.post(
            '/api/api_key',
            **{'HTTP_AUTHORIZATION': 'Basic %s' % b64_encoded_credentials.decode('utf-8')}
        ).json()['api_key']


def create_admin_account():
    return User.objects.create_superuser(*admin_test_credentials)


def create_normal_user_acount():
    return User.objects.create_user(*normal_user_credentials)


def make_request(client, query, method='GET'):
    header = {
        'HTTP_X_TAVERNATOKEN': obtain_api_key(client)
    }

    if method == 'GET':
        return client.get(endpoint, data={'query': query}, **header).json()

    if method == 'POST':
        return client.post(endpoint, data={'query': query}, **header).json()
