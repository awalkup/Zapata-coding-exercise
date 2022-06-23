import unittest
import current_weather


class MyTestCase(unittest.TestCase):
    def test_find_temp_and_pressure__ZUCK(self):
        temp_and_pressure_list = current_weather.find_temp_and_pressure("ZUCK.TXT")
        self.assertEqual(len(temp_and_pressure_list), 2)
        self.assertEqual("Temperature: 73 F (23 C)",
                         list(filter(lambda x: x.startswith("Temperature"), temp_and_pressure_list))[0])
        self.assertEqual("Pressure (altimeter): 29.71 in. Hg (1006 hPa)",
                         list(filter(lambda x: x.startswith("Pressure"), temp_and_pressure_list))[0])

    def test_find_temp_and_pressure__DRRG(self):
        temp_and_pressure_list = current_weather.find_temp_and_pressure("DRRG.TXT")
        self.assertEqual(len(temp_and_pressure_list), 0)

    def test_find_temp_and_pressure__not_a_real_file(self):
        temp_and_pressure_list = current_weather.find_temp_and_pressure("asdf.pdf")
        self.assertEqual(len(temp_and_pressure_list), 0)

    def test_find_temp_and_pressure__empty_str_file(self):
        temp_and_pressure_list = current_weather.find_temp_and_pressure("")
        self.assertEqual(len(temp_and_pressure_list), 0)

    def test_find_temp_and_pressure__file_not_str(self):
        try:
            temp_and_pressure_list = current_weather.find_temp_and_pressure(42)
            self.fail("TypeError should have been thrown")
        except TypeError:
            self.assertTrue(True)

    # Some other test ideas if we split out the URL call to mock the response:
    # send back non-text type data
    # send back multiple instances of Temperature and Pressure
    # send back the data in different formats (i.e. json)


if __name__ == '__main__':
    unittest.main()
