from base64 import b64encode

from django.contrib.auth.models import User


def obtain_api_key(client, *admin_test_credentials):
        credentials = '{}:{}'.format(
            admin_test_credentials[0],
            admin_test_credentials[2]
        )
        b64_encoded_credentials = b64encode(credentials.encode('utf-8'))

        return client.post(
            '/api/api_key',
            **{'HTTP_AUTHORIZATION': 'Basic %s' % b64_encoded_credentials.decode('utf-8')}
        ).json()['api_key']


def create_admin_account(*admin_test_credentials):
    User.objects.create_superuser(*admin_test_credentials)
