import unittest
import requests
from nanoleafapi.nanoleaf import Nanoleaf, NanoleafEffectCreationError
import json

class TestNanoleafMethods(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        # INSERT YOUR OWN VALUES HERE
        ip = '192.168.1.239'
        self.nl = Nanoleaf(ip, True)

    def test_power_on(self):
        self.assertTrue(self.nl.power_on())

    def test_power_off(self):
        self.assertTrue(self.nl.power_off())

    def test_toggle_power(self):
        self.assertTrue(self.nl.toggle_power())

    def test_set_color(self):
        self.assertTrue(self.nl.set_color((255, 255, 255)))
        self.assertFalse(self.nl.set_color((255, 255, 276)))
        self.assertFalse(self.nl.set_color((255, 255, -234)))

    def test_set_brightness(self):
        self.assertTrue(self.nl.set_brightness(100))
        with self.assertRaises(ValueError):
            self.nl.set_brightness(-10)

    def test_increment_brightness(self):
        self.assertTrue(self.nl.increment_brightness(10))
        self.assertTrue(self.nl.increment_brightness(-20))
        self.assertTrue(self.nl.increment_brightness(200))
        self.assertTrue(self.nl.increment_brightness(-300))

    def test_identify(self):
        self.assertTrue(self.nl.identify())

    def test_set_hue(self):
        self.assertTrue(self.nl.set_hue(100))
        with self.assertRaises(ValueError):
            self.nl.set_hue(-10)

    def test_increment_hue(self):
        self.assertTrue(self.nl.increment_hue(10))
        self.assertTrue(self.nl.increment_hue(-20))
        self.assertTrue(self.nl.increment_hue(200))
        self.assertTrue(self.nl.increment_hue(-300))

    def test_set_saturation(self):
        self.assertTrue(self.nl.set_saturation(100))
        with self.assertRaises(ValueError):
            self.nl.set_saturation(-10)

    def test_increment_saturation(self):
        self.assertTrue(self.nl.increment_saturation(10))
        self.assertTrue(self.nl.increment_saturation(-20))
        self.assertTrue(self.nl.increment_saturation(200))
        self.assertTrue(self.nl.increment_saturation(-300))

    def test_set_color_temp(self):
        self.assertTrue(self.nl.set_color_temp(6500))
        with self.assertRaises(ValueError):
            self.nl.set_color_temp(1100)

    def increment_color_temp(self):
        self.assertTrue(self.nl.increment_color_temp(10))
        self.assertTrue(self.nl.increment_color_temp(-20))
        self.assertTrue(self.nl.increment_color_temp(200))
        self.assertTrue(self.nl.increment_color_temp(-300))

    def test_set_effect(self):
        self.assertFalse(self.nl.set_effect('non-existent-effect'))

    def test_get_info(self):
        self.assertTrue(self.nl.get_info())

    def test_get_power(self):
        self.assertTrue(self.nl.get_power())

    def test_get_brightness(self):
        self.nl.set_brightness(100)
        self.assertEqual(self.nl.get_brightness(), 100)

    def test_get_hue(self):
        self.nl.set_hue(100)
        self.assertEqual(self.nl.get_hue(), 100)

    def test_get_saturation(self):
        self.nl.set_saturation(100)
        self.assertEqual(self.nl.get_saturation(), 100)

    def test_get_color_temp(self):
        self.assertTrue(self.nl.get_color_temp())

    def test_get_color_mode(self):
        self.assertTrue(self.nl.get_color_mode())

    def test_get_current_effect(self):
        self.assertTrue(self.nl.get_current_effect())

    def test_list_effects(self):
        self.assertTrue(self.nl.list_effects())

    def test_pulsate(self):
        self.assertTrue(self.nl.pulsate((255, 0, 0), 1))

    def test_flow(self):
        self.assertTrue(self.nl.pulsate([(255, 0, 0), (0, 255, 0)], 1))

    def test_spectrum(self):
        self.assertTrue(self.nl.pulsate(1))

    def test_write_effect(self):
        effect_data = {
            "command": "display",
            "animName": "New animation",
            "animType": "random",
            "colorType": "HSB",
            "animData": None,
            "palette": [
                {
                    "hue": 0,
                    "saturation": 100,
                    "brightness": 100
                },
                {
                    "hue": 120,
                    "saturation": 100,
                    "brightness": 100
                },
                {
                    "hue": 240,
                    "saturation": 100,
                    "brightness": 100
                }
            ],
            "brightnessRange": {
                "minValue": 25,
                "maxValue": 100
            },
            "transTime": {
                "minValue": 25,
                "maxValue": 100
            },
            "delayTime": {
                "minValue": 25,
                "maxValue": 100
            },
            "loop": True
        }
        self.assertTrue(self.nl.write_effect(effect_data))
        with self.assertRaises(NanoleafEffectCreationError):
            self.assertFalse(self.nl.write_effect({"invalid-string": "invalid"}))

    def test_effect_exists(self):
        self.assertFalse(self.nl.effect_exists('non-existent-effect'))

    def test_get_layout(self):
        self.assertTrue(self.nl.get_layout())

    def __helper_function(self, dictionary):
        self.assertTrue(True)

    def test_register_event(self):
        with self.assertRaises(Exception):
            self.nl.register_event(self.__helper_function, [5])
        with self.assertRaises(Exception):
            self.nl.register_event(self.__helper_function, [1, 2, 3, 3, 4])
        self.nl.register_event(self.__helper_function, [1])
        self.nl.toggle_power()
