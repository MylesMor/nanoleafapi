import unittest
from nanoleafapi.nanoleaf import Nanoleaf, NanoleafEffectCreationError
from nanoleafapi.digital_twin import NanoleafDigitalTwin
import socket

class TestNanoleafMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # INSERT YOUR OWN VALUES HERE
        cls.ip = '192.168.1.70'
        cls.nl = Nanoleaf(cls.ip, None, True)
        cls.digital_twin = NanoleafDigitalTwin(cls.nl)

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
        with self.assertRaises(NanoleafEffectCreationError):
            self.nl.pulsate([(256, 0, 0)], 1)
        with self.assertRaises(NanoleafEffectCreationError):
            self.nl.pulsate([(255, 0, 0), (0, 255, 0)], 1)
        with self.assertRaises(NanoleafEffectCreationError):
            self.nl.pulsate([(255, 0)], 1)


    def test_flow(self):
        self.assertTrue(self.nl.flow([(255, 0, 0), (0, 255, 0)], 1))
        with self.assertRaises(NanoleafEffectCreationError):
            self.nl.flow([(256, 0, 0), (0, 255, 0)], 1)
        with self.assertRaises(NanoleafEffectCreationError):
            self.nl.flow([(255, 0)], 1)
        with self.assertRaises(NanoleafEffectCreationError):
            self.nl.flow([(256, 0, 0)], 1)


    def test_spectrum(self):
        self.assertTrue(self.nl.spectrum(1))

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

    def test_digital_twin_get_ids(self):
        self.assertTrue(self.digital_twin.get_ids() == self.nl.get_ids())

    def test_digital_twin_set_color(self):
        self.digital_twin.set_color(self.digital_twin.get_ids()[0], (255, 255, 255))
        self.assertTrue(
            self.digital_twin.get_color(self.digital_twin.get_ids()[0]) == (255, 255, 255)
        )

    def test_digital_twin_set_all_colors(self):
        self.digital_twin.set_all_colors((255, 255, 255))
        for panel_id in self.digital_twin.get_ids():
            self.assertTrue(self.digital_twin.get_color(panel_id) == (255, 255, 255))
        all_colours = self.digital_twin.get_all_colors()
        for value in all_colours.values():
            self.assertTrue(value == (255, 255, 255))

    def test_digital_twin_sync(self):
        self.digital_twin.set_all_colors((255, 255, 255))
        self.assertTrue(self.digital_twin.sync())

    def test_ext_control(self):
        nanoleaf_udp_port = 60222
        nanoleaf_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)

        self.nl.enable_extcontrol()

        panel_ids = self.nl.get_ids()
        n_panels = len(panel_ids) - 1
        n_panels_b = n_panels.to_bytes(2, "big")

        send_data = b""
        send_data += n_panels_b
        transition = 1
        for panel_id in panel_ids:
            if panel_id != 0:
                panel_id_b = panel_id.to_bytes(2, "big")
                send_data += panel_id_b
                white = 255
                w = 0
                send_data += white.to_bytes(1, "big")
                send_data += white.to_bytes(1, "big")
                send_data += white.to_bytes(1, "big")
                send_data += w.to_bytes(1, "big")
                send_data += transition.to_bytes(2, "big")

        nanoleaf_socket.sendto(send_data, (self.ip, nanoleaf_udp_port))
        nanoleaf_socket.close()
        info = self.nl.get_info()
        self.assertTrue(info['state']['brightness']['value'] == 100)
        self.assertTrue(info['state']['colorMode'] == 'effect')
        self.assertTrue(info['state']['ct']['value'] == 6500)
        self.assertTrue(info['state']['hue']['value'] == 0)
        self.assertTrue(info['state']['sat']['value'] == 0)

