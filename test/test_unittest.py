import app  # The code to test
import unittest  # The test framework


class Test_TestIncrementDecrement(unittest.TestCase):
    def test_increment(self):
        self.assertEqual(app.increment(3), 4)

    def test_decrement(self):
        self.assertEqual(app.decrement(3), 4)


if __name__ == "__main__":
    unittest.main()
