import unittest
from unittest.mock import patch, Mock
#from backend import app, course, learning_journey, positions, registration, role, skill_rewarded, skill_set, skill, staff
import backend
from backend1 import course1
#from backend.invokes import invoke_http, all_route
#import backend.invokes


class TestBackend(unittest.TestCase):

    # def setUp(self):
    #     pass

    # def tearDown(self):
    #     pass
    def test_add(self):
        result = course1.add(10,5)
        self.assertEqual(result, 15)

    


#allow us to run the whole test suite by running - python test_unittest.py
#UPDATE: don't have to cd test just run: python -m unittest test.test_unittest
if __name__ == '__main__':
    unittest.main()