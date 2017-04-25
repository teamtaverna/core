from django.test import Client, TestCase

from .utils import create_admin_account


class TimetableApiTest(TestCase):

    def setup(self):
        self.client = Client()
        create_admin_account()

    def create_timetable(self, name, cycle_length, ref_cycle_day, ref_cycle_date, vendors, admin):
        # query = '''
        #     mutation{
        #       CreateTimetable(input: {name: "%s", cycle_length: "%s",
        #       ref_cycle_day: "%s", ref_cycle_date: "%s", vendors: "%s", admin: "%s"}){
        #         dish{
        #           id,
        #           originalId,
        #           name,
        #           cycle_length
        #         }
        #       }
        #     }
        # ''' % (name, cycle_length)
        pass
