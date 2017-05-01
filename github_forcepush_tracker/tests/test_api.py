from unittest import TestCase

# todo missing lots of tests. Need tests for all endpoints.

class HookEndpointTests(TestCase):

    def test_invalid_data(self):
        pass
        # test too long data
        # test fails simple validation
        # test

    # def test_valid_case(self):
    #     with open('sampled_force_push_event.txt') as f:
    #         data = f.readlines()
    #



class DBTests(TestCase):

    def test_db_issues(self):
        pass
        # test connection to db fails
        # test db file not readable
        # test no db
