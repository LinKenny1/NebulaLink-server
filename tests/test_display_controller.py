# tests/test_display_controller.py

import unittest
from src.controllers.display_controller import DisplayController
from src.utils import DisplayControlError


class TestDisplayController(unittest.TestCase):
    def setUp(self):
        self.controller = DisplayController()

    def test_get_display_info(self):
        displays = self.controller.get_display_info()
        print(displays)
        self.assertIsInstance(displays, list)
        self.assertTrue(len(displays) > 0)
        for display in displays:
            self.assertIn("id", display)
            self.assertIn("name", display)
            self.assertIn("friendly_name", display)
            self.assertIn("resolution", display)
            self.assertIn("refresh_rate", display)

    def test_set_resolution(self):
        # This test will actually change your display resolution, so be careful!
        # Uncomment to test, and make sure to change it back afterwards
        # original_info = self.controller.get_display_info()[0]
        # result = self.controller.set_resolution(0, 1920, 1080)
        # self.assertEqual(result['status'], 'success')
        # new_info = self.controller.get_display_info()[0]
        # self.assertEqual(new_info['resolution'], '1920x1080')
        # Restore original resolution
        # self.controller.set_resolution(0, int(original_info['resolution'].split('x')[0]),
        #                                int(original_info['resolution'].split('x')[1]))
        pass

    def test_set_refresh_rate(self):
        # This test will actually change your display refresh rate, so be careful!
        # Uncomment to test, and make sure to change it back afterwards
        # original_info = self.controller.get_display_info()[0]
        # result = self.controller.set_refresh_rate(0, 60)
        # self.assertEqual(result['status'], 'success')
        # new_info = self.controller.get_display_info()[0]
        # self.assertEqual(new_info['refresh_rate'], 60)
        # Restore original refresh rate
        # self.controller.set_refresh_rate(0, original_info['refresh_rate'])
        pass

    def test_enable_disable_dummy_display(self):
        # These are placeholder implementations, so we're just checking if they run without errors
        result = self.controller.enable_dummy_display()
        self.assertEqual(result["status"], "success")
        result = self.controller.disable_dummy_display()
        self.assertEqual(result["status"], "success")

    def test_invalid_display_id(self):
        with self.assertRaises(DisplayControlError):
            self.controller.set_resolution(999, 1920, 1080)
        with self.assertRaises(DisplayControlError):
            self.controller.set_refresh_rate(999, 60)


if __name__ == "__main__":
    unittest.main()
