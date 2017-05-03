from django.test import Client, TestCase

from .utils import create_admin_account, make_request
from app.timetables.factories import WeekdayFactory, VendorFactory, UserFactory


class TimetableApiTest(TestCase):

    def setUp(self):
        self.client = Client()
        create_admin_account()
        self.weekday = WeekdayFactory()
        self.vendor = VendorFactory()
        self.admin = UserFactory()
        self.first_timetable = self.create_timetable('test1', 'testcode1', 5, 2,
                                                     '2017-04-26', self.weekday.id,
                                                     self.vendor.id, self.admin.id)['timetable']

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

    def retrieve_timetable(self, timetable_id):
        query = 'query {timetable(id: "%s") {name}}' % (timetable_id)

        return make_request(self.client, query)

    def test_creation_of_timetable_object(self):
        response = self.create_timetable('test', 'testcode', 5, 2,
                                         '2017-04-26', self.weekday.id,
                                         self.vendor.id, self.admin.id)
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
                                'originalId': self.weekday.id
                            }
                        }
                    ]
                },
                'vendors': {
                    'edges': [
                        {
                            'node': {
                                'originalId': self.vendor.id
                            }
                        }
                    ]
                },
                'admins': {
                    'edges': [
                        {
                            'node': {
                                'originalId': self.admin.id
                            }
                        }
                    ]
                }
            }
        }
        self.assertEqual(expected, response)

        # For existing timetable record
        self.assertEqual({'timetable': None},
                         self.create_timetable('test1', 'testcode1', 5, 2,
                                               '2017-04-26', self.weekday.id,
                                               self.vendor.id, self.admin.id))

    def test_retrieve_timetable_object(self):
        response = self.retrieve_timetable(self.first_timetable['id'])
        expected = {
            'timetable': {
                'name': self.first_timetable['name']
            }
        }
        self.assertEqual(expected, response)

        # Retrieve with invalid id
        self.assertEqual({'timetable': None}, self.retrieve_timetable(100))
