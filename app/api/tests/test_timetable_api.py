from django.test import Client, TestCase

from .utils import obtain_api_key, create_admin_account


class TimetableApiTest(TestCase):

    def setup(self):
        self.client = Client()
        self.endpoint = '/api'
        self.admin_test_credentials = ('admin', 'admin@taverna.com', 'qwerty123')
        create_admin_account(*self.admin_test_credentials)
        self.header = {
            'HTTP_X_TAVERNATOKEN': obtain_api_key(
                self.client, *self.admin_test_credentials
            )
        }

    def make_request(self, query, method='GET'):
        if method == 'GET':
            return self.client.get(self.endpoint, data={'query':query}, **self.header).json()

        if method == 'POST':
            return self.client.post(self.endpoint, data={'query':query}, **self.header).json()

    def create_timetable(self, name, cycle_length, ref_cycle_day, ref_cycle_date, vendors, admin):
        query = '''
            mutation{
              CreateTimetable(input: {name: "%s", cycle_length: "%s", ref_cycle_day: "%s", ref_cycle_date: "%s", vendors: "%s", admin: "%s"}){
                dish{
                  id,
                  originalId,
                  name,
                  cycle_length
                }
              }
            }
        ''' % (name, cycle_length)
