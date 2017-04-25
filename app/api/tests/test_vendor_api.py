from django.test import Client, TestCase

from .utils import create_admin_account, make_request


class VendorApiTest(TestCase):
    """Test for Vendor API."""

    def setUp(self):
        self.client = Client()
        create_admin_account()
        self.first_vendor = self.create_vendor('vendor1', 'info1')['vendor']
        self.vendors = (
            ('vendor2', 'info2'),
            ('vendor3', 'info3')
        )

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
        return make_request(self.client, query, 'POST')

    def retrieve_vendor(self, vendor_id):
        query = 'query {vendor(id: "%s") {name}}' % (vendor_id)

        return make_request(self.client, query)

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

        # For existing vendor record
        self.assertEqual({'vendor': None},
                         self.create_vendor('vendor1', 'info1'))

    def test_retrieve_vendor_object(self):
        # Retrieve with valid id
        response = self.retrieve_vendor(self.first_vendor['id'])
        expected = {
            'vendor': {
                'name': self.first_vendor['name']
            }
        }
        self.assertEqual(expected, response)

        # Retrieve with invalid id
        self.assertEqual({'vendor': None}, self.retrieve_vendor(100))

    def test_retrieve_multiple_vendors_without_filtering(self):
        self.create_multiple_vendors()

        query = 'query {vendors{edges{node{name}}}}'

        expected = {
            'vendors': [
                {
                    'name': self.first_vendor['name']
                },
                {
                    'name': self.vendors[0][0]
                },
                {
                    'name': self.vendors[1][0]
                }
            ]
        }

        response = make_request(self.client, query)

        self.assertEqual(expected, response)

    def test_retrieve_multiple_vendors_filter_by_name(self):
        self.create_multiple_vendors()
        query = 'query {vendors(name_Icontains: "ndor1") {edges{node{name}}}}'

        expected = {
            'vendors': [
                {
                    'name': self.first_vendor['name']
                }
            ]
        }

        response = make_request(self.client, query)

        self.assertEqual(expected, response)

    def test_update_vendor_object(self):
        # Update with valid id
        query = '''
            mutation{
                updateVendor(
                    input: {
                        id: "%s",
                        name: "vendor1_updated"
                    }
                )
                {
                    vendor{
                        id,
                        originalId,
                        name
                    }
                }
            }
        ''' % (self.first_vendor['id'])
        response = make_request(self.client, query, 'POST')
        expected = {
            'vendor': {
                'id': self.first_vendor['id'],
                'originalId': self.first_vendor['originalId'],
                'name': 'vendor1_updated'
            }
        }
        self.assertEqual(expected, response)

        # Update with invalid id
        query = '''
            mutation{
                updateVendor(
                    input: {
                        id: "%s",
                        name: "invalid_update"
                    }
                )
                {
                    vendor{
                        id,
                        originalId,
                        name
                    }
                }
            }
        ''' % (100)
        self.assertEqual({'vendor': None},
                         make_request(self.client, query, 'POST'))

    def test_deletion_vendor_object(self):
        # Delete with valid id
        query = '''
            mutation{
                deleteVendor(input: {id: "%s"}){
                    vendor{
                        name
                    }
                }
            }
        ''' % (self.first_vendor['id'])
        response = make_request(self.client, query, 'POST')
        expected = {
            'vendor': {
                'name': self.first_vendor['name']
            }
        }
        self.assertEqual(expected, response)
        self.assertEqual({'vendor': None}, self.retrieve_vendor(self.first_vendor['id']))

        # Delete with invalid id
        query = '''
            mutation{
                deleteVendor(input: {id: "%s"}){
                    vendor{
                        name
                    }
                }
            }
        ''' % (100)
        self.assertEqual({'vendor': None}, make_request(self.client, query, 'POST'))
