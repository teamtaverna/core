from django.test import Client, TestCase

from .utils import create_admin_account, make_request
from app.timetables.factories import WeekdayFactory, VendorFactory, UserFactory


class TimetableApiTest(TestCase):

    def setUp(self):
        self.client = Client()
        create_admin_account()

    def create_timetable(self, name, code, cycle_length, ref_cycle_day,
                         ref_cycle_date, inactive_weekday_id, vendor_id,
                         admin_id):
        query = '''
            mutation{
                createTimetable(input: {name: "%s", code: "%s", cycleLength: %d,
                                        refCycleDay: %d, refCycleDate: "%s",
                                        inactiveWeekdayId: %d, vendorId: %d,
                                        adminId: %d}){
                    timetable{
                        id,
                        originalId,
                        name,
                        code,
                        cycleLength,
                        refCycleDay,
                        refCycleDate,
                        inactiveWeekdays{edges{node{originalId}}},
                        vendors{edges{node{originalId}}},
                        admins{edges{node{originalId}}}
                    }
                }
            }
                ''' % (name, code, cycle_length, ref_cycle_day,
                       ref_cycle_date, inactive_weekday_id, vendor_id,
                       admin_id)
        return make_request(self.client, query, 'POST')

    # def retrieve_timetable(self, timetable_id):
    #     query = 'query {timetable(id: "%s") {name}}' % (timetable_id)

    #     return make_request(self.client, query)

    def test_creation_of_timetable_object(self):
        weekday = WeekdayFactory()
        vendor = VendorFactory()
        admin = UserFactory()
        response = self.create_timetable('test', 'testcode', 5, 2,
                                         '2017-04-26', weekday.id,
                                         vendor.id, admin.id)
        created_timetable = response['timetable']
        expected = {
            'timetable': {
                'id': created_timetable['id'],
                'originalId': created_timetable['originalId'],
                'name': 'test',
                'code': 'testcode',
                'cycleLength': 5,
                'refCycleDay': 2,
                'refCycleDate': '2017-04-26',
                'inactiveWeekdays': {
                    'edges': [
                        {
                            'node': {
                                'originalId': weekday.id
                            }
                        }
                    ]
                },
                'vendors': {
                    'edges': [
                        {
                            'node': {
                                'originalId': vendor.id
                            }
                        }
                    ]
                },
                'admins': {
                    'edges': [
                        {
                            'node': {
                                'originalId': admin.id
                            }
                        }
                    ]
                }
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
