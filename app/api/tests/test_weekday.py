from django.test import Client, TestCase


class WeekdayApiTest(TestCase):
    """Tests for Weekday API."""

    def setUp(self):
        self.client = Client()
        self.endpoint = '/api'

    def create_weekday(self, name):
        query = '''
                mutation{
                    createWeekday(input: {name: "%s"}){
                        weekday{
                            id,
                            originalId,
                            name
                        }
                    }
                }
                ''' % (name)

        return self.client.post(self.endpoint, {'query': query}).json()

    def test_creation_of_weekday_object(self):
        credentials = {
            'name': 'tuesday'
        }
        response = self.create_weekday(credentials['name'])

        expected = {
            'createWeekday': {
                'weekday': {
                    'id': response['data']['createWeekday']['weekday']['id'],
                    'originalId': response['data']['createWeekday']['weekday']['originalId'],
                    'name': credentials['name']
                }
            }
        }

        self.assertEqual(expected, response['data'])
