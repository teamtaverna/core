from django.test import Client, TestCase

from .utils import obtain_api_key, create_admin_account


class VendorApiTest(TestCase):
    """Test for Vendor API."""

    def setUp(self):
        self.client = Client()
        self.endpoint = '/api'
        self.admin_test_credentials = ('admin', 'admin@taverna.com', 'qwerty123')
        create_admin_account(*self.admin_test_credentials)
        self.header = {
            'HTTP_X_TAVERNATOKEN': obtain_api_key(
                self.client, *self.admin_test_credentials
            )
        }
        self.vendors = (
            ('vendor1', 'info1'),
            ('vendor2', 'info2')
        )

    def make_request(self, query, method='GET'):
        if method == 'GET':
            return self.client.get(self.endpoint,
                                   data={'query': query},
                                   **self.header
                                   ).json()

        if method == 'POST':
            return self.client.post(self.endpoint,
                                    data={'query': query},
                                    **self.header
                                    ).json()

    def create_vendor(self, name, info):
        query = '''
                mutation{
                    createVendor(input: {name: "%s", info: "%s"}){
                        vendor{
                            id,
                            originalId,
                            name,
                            info
                        }
                    }
                }
                ''' % (name, info)

        return self.make_request(query, 'POST')

    def retrieve_vendor(self, vendor_id):
        query = 'query {vendor(id: "%s") {name}}' % (vendor_id)

        return self.make_request(query)

    def create_multiple_vendors(self):
        return [self.create_vendor(name, info) for name, info in self.vendors]

    def test_creation_of_vendor_object(self):
        # For new vendor record
        response = self.create_vendor('vendor4', 'info4')
        created_vendor = response['vendor']
        expected = {
            'vendor': {
                'id': created_vendor['id'],
                'originalId': created_vendor['originalId'],
                'name': 'vendor4',
                'info': 'info4'
            }
        }
        self.assertEqual(expected, response)
