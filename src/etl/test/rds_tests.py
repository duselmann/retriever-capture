import unittest
# import sys
# sys.path.append("../src")

from src.etl.rds import RDS
from src.etl.rds import ValidationException


class RdsValidationTests(unittest.TestCase):

    def test_this_test_class_works(self):
        self.assertTrue(True, "works")

    def test_validate_contains_text(self):
        rds = RDS()
        rds.validate_contains("Variable", "Contains")
        self.assertTrue(True, "Should not throw exception on a variable that contains text.")

    def test_validate_contains_none(self):
        rds = RDS()
        with self.assertRaises(ValidationException, msg="Should throw exception on a variable that is None."):
            rds.validate_contains("Variable", None)

    def test_validate_int(self):
        rds = RDS()
        rds.validate_int("Variable", "100", 100, 200)
        self.assertTrue(True, "Should not throw exception on a variable that is an integer.")

    def test_validate_int_float(self):
        rds = RDS()
        with self.assertRaises(ValidationException, msg="Should throw exception on a variable that is not an integer."):
            rds.validate_int("Variable", "100.1", 100, 200)

    def test_validate_int_outside_range(self):
        rds = RDS()
        with self.assertRaises(ValidationException, msg="Should throw exception on a variable that is not an integer in range."):
            rds.validate_int("Variable", "99", 100, 200)

    def test_validate_api(self):
        rds = RDS()
        rds.validate_api("api", "https://some.net/api/call")
        self.assertTrue(True, "Should not throw an exception on an API in the URL.")

    def test_validate_api_missing(self):
        rds = RDS()
        with self.assertRaises(ValidationException, msg="Should throw an exception on an API missing in the URL."):
            rds.validate_api("api", "https://some.net/other/call")

    def test_validate_json(self):
        rds = RDS()
        rds.validate_json("Json Var", '{"json":"value"}')
        self.assertTrue(True, "Should not throw an exception on valid JSON.")

    def test_validate_json_invalid(self):
        rds = RDS()
        with self.assertRaises(ValidationException, msg="Should throw an exception on invalid JSON."):
            rds.validate_json("Json Var", 'not json')


if __name__ == '__main__':
    unittest.main()
