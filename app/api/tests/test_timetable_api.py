from django.test import Client, TestCase

from .utils import create_admin_account, make_request


class TimetableApiTest(TestCase):

    def setup(self):
        self.client = Client()
        create_admin_account()
        # self.sample_timetable = self.create_timetable('sample', 1, 1, 2017-04-26, 'mathe3', 'admin')
        # self.timetables = (
        # ('test2', 2, 2, 2017-04-27, 'mwas', 'admin'),
        # ('test4', 2, 2, 2017-04-28, 'kim', 'admin')
        # )

    def create_timetable(self, name, cycle_length, ref_cycle_day, ref_cycle_date, vendors, admin):
        query = '''
            mutation{
                createTimetable(input: {name: "%s", cycle_length: "%s",
                                        ref_cycle_day: "%s", ref_cycle_date: "%s",
                                        vendors: "%s", admin: "%s"}){
                    timetable{
                        id,
                        originalId,
                        name,
                        cycle_length,
                        ref_cycle_day,
                        ref_cycle_date,
                        vendors,
                        admin
                    }
                }
            }
                ''' % (name, cycle_length, ref_cycle_day, ref_cycle_date, vendors, admin)
        return make_request(self.client, query)

    def retrieve_timetable(self, timetable_id):
        query = 'query {timetable(id: "%s") {name}}' % (timetable_id)

        return make_request(self.client, query)

    def test_creation_of_timetable_object(self):
        response = self.create_timetable('test2', 1, 1, 2017-04-26, 'mathe2', 'admin')
        created_timetable = response['timetable']
        expected = {
            'timetable': {
                'id': created_timetable['id'],
                'originalId': created_timetable['originalId'],
                'name': 'test2',
                'refCycleDay': 1
            }
        }
        self.assertEqual(expected, response)

    # def test_retrieve_timetable_object(self):
    #     response = self.retrieve_timetable(self.sample_timetable['id'])
    #     expected = {
    #         'timetable': {
    #             'name': self.sample_timetable['name']
    #         }
    #     }
    #     self.assertEqual(expected, response)

    #     # Retrieve with invalid id
    #     self.assertEqual({'vendor': None}, self.retrieve_timetable(100))
