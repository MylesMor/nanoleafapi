"""nanoleafapi

This module is a Python 3 wrapper for the Nanoleaf OpenAPI.
It provides an easy way to use many of the functions available in the API.
It supports the Light Panels (previously Aurora), Canvas and Shapes (including Hexgaons)."""

import json
from threading import Thread
import multiprocessing
import colorsys
import os
from typing import Any, List, Dict, Tuple, Union, Callable
from sseclient import SSEClient
import requests

# Preset colours
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
LIGHT_BLUE = (173, 216, 230)
BLUE = (0, 0, 255)
PINK = (255, 192, 203)
PURPLE = (128, 0, 128)
WHITE = (255, 255, 255)

class Nanoleaf():
    """The Nanoleaf class for controlling the Light Panels and Canvas

    :ivar ip: IP of the Nanoleaf device
    :ivar url: The base URL for requests
    :ivar auth_token: The authentication token for the API
    :ivar print_errors: True for errors to be shown, otherwise False
    """

    def __init__(self, ip : str, auth_token : str =None, print_errors : bool =False):
        """Initalises Nanoleaf class with desired arguments.

        :param ip: The IP address of the Nanoleaf device
        :param auth_token: Optional, include Nanoleaf authentication
            token here if required.
        :param print_errors: Optional, True to show errors in the console

        :type ip: str
        :type auth_token: str
        :type print_errors: bool
        """
        self.ip = ip
        self.url = "http://" + ip + ":16021/api/v1/" + str(auth_token)
        self.check_connection()
        if auth_token is None:
            self.auth_token = self.create_auth_token()
            if self.auth_token is None:
                raise NanoleafRegistrationError()
        else:
            self.auth_token = auth_token
        self.url = "http://" + ip + ":16021/api/v1/" + str(self.auth_token)
        self.print_errors = print_errors
        self.already_registered = False


    def __error_check(self, code : int) -> bool:
        """Checks and displays error messages

        Determines the request status code and prints the error, if print_errors
        is true.

        :param code: The error code

        :returns: Returns True if request was successful, otherwise False
        """
        if self.print_errors:
            if code in (200, 204):
                print(str(code) + ": Action performed successfully.")
                return True
            if code == 400:
                print("Error 400: Bad request.")
            elif code == 401:
                print("Error 401: Unauthorized, invalid auth token. " +
                    "Please generate a new one.")
            elif code == 403:
                print("Error 403: Unauthorized, please hold the power " +
                    "button on the controller for 5-7 seconds, then try again.")
            elif code == 404:
                print("Error 404: Resource not found.")
            elif code == 500:
                print("Error 500: Internal server error.")
            return False
        return bool(code in (200, 204))
        

    def create_auth_token(self) -> Union[str, None]:
        """Creates or retrives the device authentication token

        The power button on the device should be held for 5-7 seconds, then
        this method should be run. This will set both the auth_token and url
        instance variables, and save the token in a file for future instances
        of the Nanoleaf object.

        :returns: Token if successful, None if not.
        """
        file_path = os.path.expanduser('~') + os.path.sep + '.nanoleaf_token'
        if os.path.exists(file_path) is False:
            open(file_path, 'w')
        token = open(file_path, 'r').read()
        if token:
            return token

        response = requests.post('http://' + self.ip + ':16021/api/v1/new')

        # process response
        if response and response.status_code == 200:
            data = json.loads(response.text)

            if 'auth_token' in data:
                open(file_path, 'w').write(data['auth_token'])
                return data['auth_token']
        return None

    def delete_auth_token(self, auth_token : str =None) -> bool:
        """Deletes an authentication token

        Deletes an authentication token and the .nanoleaf_token file if it
        contains the auth token to delete. This token can no longer be used
        as part of an API call to control the device. If required, generate
        a new one using create_auth_token().

        :param auth_token: Optional, the authentication token to delete, otherwise
            delete currently initialised one

        :returns: True if successful, otherwise False
        """
        file_path = os.path.expanduser('~') + os.path.sep + '.nanoleaf_token'
        if os.path.exists(file_path):
            token = open(file_path, 'r').read()
            if (auth_token is None and self.auth_token == token) or (auth_token == token):
                os.remove(file_path)
        if auth_token is None:
            url = "http://" + self.ip + ":16021/api/v1/" + str(self.auth_token)
        else:
            url = "http://" + self.ip + ":16021/api/v1/" + str(auth_token)
        response = requests.delete(url)
        return self.__error_check(response.status_code)

    def check_connection(self) -> None:
        """Ensures there is a valid connection"""
        try:
            requests.get(self.url, timeout=5)
        except Exception as connection_error:
            raise NanoleafConnectionError() from connection_error

    def get_info(self) -> Dict[str, Any]:
        """Returns a dictionary of device information"""
        response = requests.get(self.url)
        return json.loads(response.text)

    def get_name(self) -> str:
        """Returns the name of the current device"""
        return self.get_info()['name']

    def get_auth_token(self) -> str:
        """Returns the current auth token"""
        return self.auth_token

    def get_ids(self) -> List[int]:
        """Returns a list of all device ids"""
        position_data = []
        device_ids = []
        info_data = self.get_info()

        if ('panelLayout' in info_data and 'layout' in info_data['panelLayout'] and
                'positionData' in info_data['panelLayout']['layout']):
            position_data = info_data['panelLayout']['layout']['positionData']

        # process position data
        for data in position_data:
            device_ids.append(data['panelId'])

        return device_ids

    @staticmethod
    def get_custom_base_effect(anim_type : str ='custom', loop : bool =True) -> Dict[str, Any]:
        """Returns base custom effect dictionary"""
        base_effect = {
            'command': 'display',
            'animType': anim_type,
            'loop': loop,
            'palette': []
        }
        return base_effect


    #######################################################
    ####                    POWER                      ####
    #######################################################

    def power_off(self) -> bool:
        """Powers off the lights

        :returns: True if successful, otherwise False
        """
        data = {"on" : {"value": False}}
        response = requests.put(self.url + "/state", data=json.dumps(data))
        return self.__error_check(response.status_code)

    def power_on(self) -> bool:
        """Powers on the lights

        :returns: True if successful, otherwise False
        """
        data = {"on" : {"value": True}}
        response = requests.put(self.url + "/state", data=json.dumps(data))
        return self.__error_check(response.status_code)

    def get_power(self) -> bool:
        """Returns the power status of the lights

        :returns: True if on, False if off
        """
        response = requests.get(self.url + "/state/on")
        ans = json.loads(response.text)
        return ans['value']

    def toggle_power(self) -> bool:
        """Toggles the lights on/off"""
        if self.get_power():
            return self.power_off()
        return self.power_on()

    #######################################################
    ####                   COLOUR                      ####
    #######################################################

    def set_color(self, rgb : Tuple[int, int, int]) -> bool:
        """Sets the colour of the lights

        :param rgb: Tuple in the format (r, g, b)

        :returns: True if successful, otherwise False
        """
        hsv_colour = colorsys.rgb_to_hsv(rgb[0]/255, rgb[1]/255, rgb[2]/255)
        hsv_colour_list = list(hsv_colour)
        hsv_colour_list[0] *= 360
        hsv_colour_list[1] *= 100
        hsv_colour_list[2] *= 100
        final_colour = [ int(x) for x in hsv_colour_list ]
        data = {
                    "hue" : {"value": final_colour[0]},
                    "sat": {"value": final_colour[1]},
                    "brightness": {"value": final_colour[2], "duration": 0}
                }
        response = requests.put(self.url + "/state", data=json.dumps(data))
        return self.__error_check(response.status_code)

    #######################################################
    ####               ADJUST BRIGHTNESS               ####
    #######################################################

    def set_brightness(self, brightness : int, duration : int =0) -> bool:
        """Sets the brightness of the lights

        :param brightness: The required brightness (between 0 and 100)
        :param duration: The duration over which to change the brightness

        :returns: True if successful, otherwise False
        """
        if brightness > 100 or brightness < 0:
            raise ValueError('Brightness should be between 0 and 100')
        data = {"brightness" : {"value": brightness, "duration": duration}}
        response = requests.put(self.url + "/state", data=json.dumps(data))
        return self.__error_check(response.status_code)

    def increment_brightness(self, brightness : int) -> bool:
        """Increments the brightness of the lights

        :param brightness: How much to increment the brightness, can
            also be negative

        :returns: True if successful, otherwise False
        """
        data = {"brightness" : {"increment": brightness}}
        response = requests.put(self.url + "/state", data = json.dumps(data))
        return self.__error_check(response.status_code)

    def get_brightness(self) -> int:
        """Returns the current brightness value of the lights"""
        response = requests.get(self.url + "/state/brightness")
        ans = json.loads(response.text)
        return ans['value']

    #######################################################
    ####                  IDENTIFY                     ####
    #######################################################

    def identify(self) -> bool:
        """Runs the identify sequence on the lights

        :returns: True if successful, otherwise False
        """
        response = requests.put(self.url + "/identify")
        return self.__error_check(response.status_code)

    #######################################################
    ####                    HUE                        ####
    #######################################################

    def set_hue(self, value : int) -> bool:
        """Sets the hue of the lights

        :param value: The required hue (between 0 and 360)

        :returns: True if successful, otherwise False
        """
        if value > 360 or value < 0:
            raise ValueError('Hue should be between 0 and 360')
        data = {"hue" : {"value" : value}}
        response = requests.put(self.url + "/state", data=json.dumps(data))
        return self.__error_check(response.status_code)

    def increment_hue(self, value : int) -> bool:
        """Increments the hue of the lights

        :param value: How much to increment the hue, can also be negative

        :returns: True if successful, otherwise False
        """
        data = {"hue" : {"increment" : value}}
        response = requests.put(self.url + "/state", data=json.dumps(data))
        return self.__error_check(response.status_code)

    def get_hue(self) -> int:
        """Returns the current hue value of the lights"""
        response = requests.get(self.url + "/state/hue")
        ans = json.loads(response.text)
        return ans['value']

    #######################################################
    ####                 SATURATION                    ####
    #######################################################

    def set_saturation(self, value : int) -> bool:
        """Sets the saturation of the lights

        :param value: The required saturation (between 0 and 100)

        :returns: True if successful, otherwise False
        """
        if value > 100 or value < 0:
            raise ValueError('Saturation should be between 0 and 100')
        data = {"sat" : {"value" : value}}
        response = requests.put(self.url + "/state", data=json.dumps(data))
        return self.__error_check(response.status_code)

    def increment_saturation(self, value : int) -> bool:
        """Increments the saturation of the lights

        :param brightness: How much to increment the saturation, can also be
            negative.

        :returns: True if successful, otherwise False
        """
        data = {"sat" : {"increment" : value}}
        response = requests.put(self.url + "/state", data=json.dumps(data))
        return self.__error_check(response.status_code)

    def get_saturation(self) -> int:
        """Returns the current saturation value of the lights"""
        response = requests.get(self.url + "/state/sat")
        ans = json.loads(response.text)
        return ans['value']

    #######################################################
    ####              COLOUR TEMPERATURE               ####
    #######################################################

    def set_color_temp(self, value : int) -> bool:
        """Sets the white colour temperature of the lights

        :param value: The required colour temperature (between 0 and 100)

        :returns: True if successful, otherwise False
        """
        if value > 6500 or value < 1200:
            raise ValueError('Colour temp should be between 1200 and 6500')
        data = {"ct" : {"value" : value}}
        response = requests.put(self.url + "/state", json.dumps(data))
        return self.__error_check(response.status_code)

    def increment_color_temp(self, value : int) -> bool:
        """Sets the white colour temperature of the lights

        :param value: How much to increment the colour temperature by, can also
            be negative.

        :returns: True if successful, otherwise False
        """
        data = {"ct" : {"increment" : value}}
        response = requests.put(self.url + "/state", json.dumps(data))
        return self.__error_check(response.status_code)

    def get_color_temp(self) -> int:
        """Returns the current colour temperature of the lights"""
        response = requests.get(self.url + "/state/ct")
        ans = json.loads(response.text)
        return ans['value']

    #######################################################
    ####                 COLOUR MODE                   ####
    #######################################################

    def get_color_mode(self) -> str:
        """Returns the colour mode of the lights"""
        response = requests.get(self.url + "/state/colorMode")
        return json.loads(response.text)

    #######################################################
    ####                   EFFECTS                     ####
    #######################################################

    def get_current_effect(self) -> str:
        """Returns the currently selected effect

        If the name of the effect isn't available, this will return
        *Solid*, *Dynamic* or *Static* instead.

        :returns: Name of the effect or type if unavailable.
        """
        response = requests.get(self.url + "/effects/select")
        return json.loads(response.text)

    def set_effect(self, effect_name : str) -> bool:
        """Sets the effect of the lights

        :param effect_name: The name of the effect

        :returns: True if successful, otherwise False
        """
        data = {"select": effect_name}
        response = requests.put(self.url + "/effects", data=json.dumps(data))
        return self.__error_check(response.status_code)

    def list_effects(self) -> List[str]:
        """Returns a list of available effects"""
        response = requests.get(self.url + "/effects/effectsList")
        return json.loads(response.text)

    def write_effect(self, effect_dict : Dict['str', Any]) -> bool:
        """Writes a user-defined effect to the panels

        :param effect_dict: The effect dictionary in the format
            described here: https://forum.nanoleaf.me/docs/openapi#_u2t4jzmkp8nt

        :raises NanoleafEffectCreationError: When invalid effect dictionary is provided.

        :returns: True if successful, otherwise False
        """
        response = requests.put(self.url + "/effects", data=json.dumps({"write": effect_dict}))
        if response.status_code == 400:
            raise NanoleafEffectCreationError("Invalid effect dictionary")
        return self.__error_check(response.status_code)

    def effect_exists(self, effect_name : str) -> bool:
        """Verifies whether an effect exists

        :param effect_name: Name of the effect to verify

        :returns: True if effect exists, otherwise False
        """
        response = requests.get(self.url + "/effects/effectsList")
        if effect_name in json.loads(response.text):
            return True
        return False

    def pulsate(self, rgb : Tuple[int, int, int], speed : float = 1) -> bool:
        """Displays a pulsating effect on the device with two colours

        :param rgb: A tuple containing the RGB colour to pulsate in the format (r, g, b).
        :param speed: The speed of the transition between colours in seconds,
            with a maximum of 1 decimal place.

        :raises NanoleafEffectCreationError: When an invalid rgb value is provided.

        :returns: True if the effect was created and displayed successfully, otherwise False
        """
        if len(rgb) != 3:
            raise NanoleafEffectCreationError("There must be three values in the " +
                "RGB tuple! E.g., (255, 0, 0)")
        for colour in rgb:
            if not isinstance(colour, int):
                raise NanoleafEffectCreationError("All values in the tuple must be " +
                    "integers! E.g., (255, 0, 0)")
            if colour < 0 or colour > 255:
                raise NanoleafEffectCreationError("All values in the tuple must be  " +
                    "integers between 0 and 255! E.g., (255, 0, 0)")
        base_effect = self.get_custom_base_effect()
        ids = self.get_ids()
        anim_data = str(len(ids))
        frame_string = ""
        for device_id in ids:
            frame_string += " {id} 2".format(id=device_id)
            r, g, b = rgb[0], rgb[1], rgb[2]
            frame_string += " {r} {g} {b} 0 {speed} 0 0 0 0 {speed_2}".format(
                    r=r, g=g, b=b, speed=int(speed*10), speed_2=int(speed*10))
        base_effect['animData'] = anim_data + frame_string
        return self.write_effect(base_effect)

    def flow(self, rgb_list : List[Tuple[int, int, int]], speed : float = 1) -> bool:
        """Displays a sequence of specified colours on the device.

        :param rgb: A list of tuples containing RGB colours to flow between in the format (r, g, b).
        :param speed: The speed of the transition between colours in seconds, with a maximum of
            1 decimal place.

        :raises NanoleafEffectCreationError: When an invalid rgb_list is provided.

        :returns: True if the effect was created and displayed successfully, otherwise False
        """
        if len(rgb_list) <= 1:
            raise NanoleafEffectCreationError("There has to be more than one tuple in " +
                "the RGB list for this effect! E.g., [(255, 0, 0), (0, 0, 0)]")
        for tup in rgb_list:
            if len(tup) != 3:
                raise NanoleafEffectCreationError("There must be three values in the " +
                    "RGB tuple! E.g., (255, 0, 0)")
            for colour in tup:
                if not isinstance(colour, int):
                    raise NanoleafEffectCreationError("All values in the tuple must " +
                        "be integers! E.g., (255, 0, 0)")
                if colour < 0 or colour > 255:
                    raise NanoleafEffectCreationError("All values in the tuple must " +
                        "be integers between 0 and 255! E.g., (255, 0, 0)")
        base_effect = self.get_custom_base_effect()
        ids = self.get_ids()
        anim_data = str(len(ids))
        frame_string = ""
        for device_id in ids:
            frame_string += " {id} {numFrames}".format(id=device_id, numFrames=len(rgb_list))
            for rgb in rgb_list:
                r, g, b = rgb[0], rgb[1], rgb[2]
                frame_string += " {r} {g} {b} 0 {speed}".format(r=r, g=g, b=b, speed=int(speed*10))
        base_effect['animData'] = anim_data + frame_string
        return self.write_effect(base_effect)

    def spectrum(self, speed : float = 1) -> bool:
        """Displays a spectrum cycling effect on the device

        :param speed: The speed of the transition between colours in seconds,
            with a maximum of 1 decimal place.

        :returns: True if the effect was created and displayed successfully,
            otherwise False
        """
        base_effect = self.get_custom_base_effect()
        ids = self.get_ids()
        spectrum_palette = []
        for hue in range(0, 360, 10):
            (r, g, b) = colorsys.hsv_to_rgb(hue/360, 1.0, 1.0)
            spectrum_palette.append((int(255*r), int(255*g), int(255*b)))
        anim_data = str(len(ids))
        frame_string = ""
        for device_id in ids:
            frame_string += " {id} {numFrames}".format(id=device_id,
                numFrames=len(spectrum_palette))
            for rgb in spectrum_palette:
                r, g, b = rgb[0], rgb[1], rgb[2]
                frame_string += " {r} {g} {b} 0 {speed}".format(r=r, g=g, b=b, speed=int(speed*10))
        base_effect['animData'] = anim_data + frame_string
        return self.write_effect(base_effect)

    #######################################################
    ####                  LAYOUT                       ####
    #######################################################

    def get_layout(self) -> Dict[str, Any]:
        """Returns the device layout information"""
        response = requests.get(self.url + "/panelLayout/layout")
        return json.loads(response.text)

    #######################################################
    ####                  EVENTS                       ####
    #######################################################

    def register_event(self, func : Callable[[Dict[str, Any]], Any],
        event_types : List[int]) -> None:
        """Starts a thread to register and listen for events

        Creates an event listener. This method can only be called once per
        program run due to API limitations.

        :param func: The function to run when an event is recieved (this
            should be defined by the user with one argument). This function
            will recieve the event as a dictionary.
        :param event_types: A list containing up to 4 numbers from
            1-4 corresponding to the relevant events to be registered for.
            1 = state (power/brightness),
            2 = layout,
            3 = effects,
            4 = touch (Canvas only)
        """

        if self.already_registered:
            print("Cannot register events more than once.")
            return
        if len(event_types) > 4 or len(event_types) < 1:
            raise Exception("The number of events to register for must be" +
                "between 1-4")
        for event in event_types:
            if event < 1 or event > 4:
                raise Exception("Valid event types must be between 1-4")
        self.already_registered = True
        thread = Thread(target=self.__event_listener, args=(func, set(event_types)))
        thread.daemon = True
        thread.start()

    def __event_listener(self, func : Callable[[Dict[str, Any]], Any],
        event_types : List[int]) -> Callable[[], Any]:
        """Listens for events and passes event data to the user-defined
        function."""
        url = self.url + "/events?id="
        for event in event_types:
            url += str(event) + ","
        client = SSEClient(url[:-1])
        for event in client:
            func(json.loads(str(event)))


#######################################################
####                   ERRORS                      ####
#######################################################

class NanoleafRegistrationError(Exception):
    """Raised when an issue during device registration."""

    def __init__(self) -> None:
        message = """Authentication token generation failed. Hold the power
            button on your Nanoleaf device for 5-7 seconds and try again."""
        super().__init__(message)


class NanoleafConnectionError(Exception):
    """Raised when the connection to the Nanoleaf device fails."""

    def __init__(self) -> None:
        message = "Connection to Nanoleaf device failed. Is this the correct IP?"
        super().__init__(message)


class NanoleafEffectCreationError(Exception):
    """Raised when one of the custom effects creation has incorrect arguments."""
