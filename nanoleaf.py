import requests
import json
from sseclient import SSEClient
from threading import Thread
import colorsys

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

    def __init__(self, ip, auth_token=None, print_errors=False):
        """Initalises Nanoleaf class with desired arguments.

        :param ip: The IP address of the Nanoleaf device
        :param auth_token: Optional, include Nanoleaf authentication
            token here if generated, otherwise call generate_auth_token()
            after initlisation
        :param print_errors: Optional, True to show errors in the console

        :type ip: str
        :type auth_token: str
        :type print_errors: bool
        """
        self.ip = ip
        self.url = "http://" + ip + ":16021/api/v1/" + str(auth_token)
        self.auth_token = auth_token
        self.print_errors = print_errors
        self.already_registered = False
        try:
            self.__check_connection()
        except:
            raise Exception("No valid Nanoleaf device found on IP: " + self.ip)



    def __error_check(self, code):
        """Checks and displays error messages

        Determines the request status code and prints the error, if print_errors
        is true.

        :param code: The error code

        :returns: Returns True if request was successful, otherwise False
        """
        if self.print_errors:
            if code == 200 or code == 204:
                print("Action performed successfully.")
                return True
            elif code == 400:
                print("Error 400: Bad request.")
            elif code == 401:
                print("Error 401: Unauthorized, incorrect auth token. " +
                    "Please generate a new one.")
            elif code == 403:
                print("Unauthorized, please hold the power button on the controller for 5-7 seconds, then try again.")
            elif code == 404:
                print("Error 404: Resource not found.")
            elif code == 500:
                print("Error 500: Internal server error.")
            return False
        else:
            if code == 200 or code == 204:
                return True
            else:
                return False

    def generate_auth_token(self):
        """Generates authentication token for device

        The power button on the device should be held for 5-7 seconds, then
        this method should be run. This will set both the auth_token and url
        instance variables. The authentication token printed in the console
        should be stored for use in own program and future instances of this
        class should initalised using this.

        :returns: True if successful, otherwise False
        """
        url = "http://" + self.ip + ":16021/api/v1/new"
        r = requests.post(url)
        if r.status_code == 200:
            self.auth_token = json.loads(r.text)['auth_token']
            print("Auth token successfully generated! Token: " + self.auth_token)
            self.url = "http://" + self.ip + ":16021/api/v1/" + str(self.auth_token)
            return True
        else:
            return self.__error_check(r.status_code)


    def delete_user(self, auth_token):
        """Deletes an authentication token

        Deletes an authentication token. This token can no longer be used
        as part of an API call to control the device. If required, generate
        a new one using generate_auth_token().

        :param auth_token: The authentication token to delete

        :returns: True if successful, otherwise False
        """
        url = "http://" + self.ip + ":16021/api/v1/" + str(auth_token)
        r = requests.delete(url)
        return self.__error_check(r.status_code)

    def __check_connection(self):
        """Ensures there is a valid connection"""
        requests.get(self.url, timeout=5)

    def get_panel_info(self):
        """Returns a dictionary of device information"""
        r = requests.get(self.url)
        return json.loads(r.text)

    #######################################################
    ####                    POWER                      ####
    #######################################################

    def power_off(self):
        """Powers off the lights

        :returns: True if successful, otherwise False
        """
        data = {"on" : {"value": False}}
        r = requests.put(self.url + "/state", data=json.dumps(data))
        return self.__error_check(r.status_code)

    def power_on(self):
        """Powers on the lights

        :returns: True if successful, otherwise False
        """
        data = {"on" : {"value": True}}
        r = requests.put(self.url + "/state", data=json.dumps(data))
        return self.__error_check(r.status_code)

    def get_power(self):
        """Returns the power status of the lights

        :returns: True if on, False if off
        """
        r = requests.get(self.url + "/state/on")
        ans = json.loads(r.text)
        return ans['value']

    def toggle_power(self):
        """Toggles the lights on/off"""
        if self.get_power():
            self.power_off()
        else:
            self.power_on()

    #######################################################
    ####                   COLOUR                      ####
    #######################################################

    def set_color(self, rgb):
        """Sets the colour of the lights

        :param rgb: Tuple in the format (r, g, b)

        :returns: True if successful, otherwise False
        """
        hsv_colour = colorsys.rgb_to_hsv(rgb[0]/255, rgb[1]/255, rgb[2]/255)
        hsv_colour = list(hsv_colour)
        hsv_colour[0] *= 360
        hsv_colour[1] *= 100
        hsv_colour[2] *= 100
        final_colour = [ int(x) for x in hsv_colour ]
        data = {
                    "hue" : {"value": final_colour[0]},
                    "sat": {"value": final_colour[1]},
                    "brightness": {"value": final_colour[2], "duration": 0}
                }
        r = requests.put(self.url + "/state", data=json.dumps(data))
        return self.__error_check(r.status_code)

    #######################################################
    ####               ADJUST BRIGHTNESS               ####
    #######################################################

    def set_brightness(self, brightness, duration=0):
        """Sets the brightness of the lights

        :param brightness: The required brightness (between 0 and 100)
        :param duration: The duration over which to change the brightness

        :returns: True if successful, otherwise False
        """
        if brightness > 100 or brightness < 0:
            raise Exception('Brightness should be between 0 and 100')
        data = {"brightness" : {"value": brightness, "duration": duration}}
        r = requests.put(self.url + "/state", data=json.dumps(data))
        return self.__error_check(r.status_code)

    def increment_brightness(self, brightness):
        """Increments the brightness of the lights

        :param brightness: How much to increment the brightness, can
            also be negative

        :returns: True if successful, otherwise False
        """
        data = {"brightness" : {"increment": brightness}}
        r = requests.put(self.url + "/state", data = json.dumps(data))
        return self.__error_check(r.status_code)

    def get_brightness(self):
        """Returns the current brightness value of the lights"""
        r = requests.get(self.url + "/state/brightness")
        ans = json.loads(r.text)
        return ans['value']

    #######################################################
    ####                  IDENTIFY                     ####
    #######################################################

    def identify(self):
        """Runs the identify sequence on the lights

        :returns: True if successful, otherwise False
        """
        r = requests.put(self.url + "/identify")
        return self.__error_check(r.status_code)

    #######################################################
    ####                    HUE                        ####
    #######################################################

    def set_hue(self, value):
        """Sets the hue of the lights

        :param value: The required hue (between 0 and 360)

        :returns: True if successful, otherwise False
        """
        if value > 360 or value < 0:
            raise Exception('Hue should be between 0 and 360')
        data = {"hue" : {"value" : value}}
        r = requests.put(self.url + "/state", data=json.dumps(data))
        return self.__error_check(r.status_code)

    def increment_hue(self, value):
        """Increments the hue of the lights

        :param value: How much to increment the hue, can also be negative

        :returns: True if successful, otherwise False
        """
        data = {"hue" : {"increment" : value}}
        r = requests.put(self.url + "/state", data=json.dumps(data))
        return self.__error_check(r.status_code)

    def get_hue(self):
        """Returns the current hue value of the lights"""
        r = requests.get(self.url + "/state/hue")
        ans = json.loads(r.text)
        return ans['value']

    #######################################################
    ####                 SATURATION                    ####
    #######################################################

    def set_saturation(self, value):
        """Sets the saturation of the lights

        :param value: The required saturation (between 0 and 100)

        :returns: True if successful, otherwise False
        """
        if value > 100 or value < 0:
            raise Exception('Saturation should be between 0 and 100')
        data = {"sat" : {"value" : value}}
        r = requests.put(self.url + "/state", data=json.dumps(data))
        return self.__error_check(r.status_code)

    def increment_saturation(self, value):
        """Increments the saturation of the lights

        :param brightness: How much to increment the saturation, can also be
            negative.

        :returns: True if successful, otherwise False
        """
        data = {"sat" : {"increment" : value}}
        r = requests.put(self.url + "/state", data=json.dumps(data))
        return self.__error_check(r.status_code)

    def get_saturation(self):
        """Returns the current saturation value of the lights"""
        r = requests.get(self.url + "/state/sat")
        ans = json.loads(r.text)
        return ans['value']

    #######################################################
    ####              COLOUR TEMPERATURE               ####
    #######################################################

    def set_color_temp(self, value):
        """Sets the white colour temperature of the lights

        :param value: The required colour temperature (between 0 and 100)

        :returns: True if successful, otherwise False
        """
        if value > 6500 or value < 1200:
            raise Exception('Brightness should be between 1200 and 6500')
        data = {"ct" : {"value" : value}}
        r = requests.put(self.url + "/state", json.dumps(data))
        return self.__error_check(r.status_code)

    def increment_color_temp(self, value):
        """Sets the white colour temperature of the lights

        :param value: How much to increment the colour temperature by, can also
            be negative.

        :returns: True if successful, otherwise False
        """
        data = {"ct" : {"increment" : value}}
        r = requests.put(self.url + "/state", json.dumps(data))
        return self.__error_check(r.status_code)

    def get_color_temp(self):
        """Returns the current colour temperature of the lights"""
        r = requests.get(self.url + "/state/ct")
        ans = json.loads(r.text)
        return ans['value']

    #######################################################
    ####                 COLOUR MODE                   ####
    #######################################################

    def get_color_mode(self):
        """Returns the colour mode of the lights"""
        response = requests.get(self.url + "/state/colorMode")
        return json.loads(response.text)

    #######################################################
    ####                   EFFECTS                     ####
    #######################################################

    def get_current_effect(self):
        """Returns the currently selected effect

        If the name of the effect isn't available, this will return
        *Solid*, *Dynamic* or *Static* instead.

        :returns: Name of the effect or type if unavailable.
        """
        r = requests.get(self.url + "/effects/select")
        return json.loads(r.text)

    def set_effect(self, effect_name):
        """Sets the effect of the lights

        :param effect_name: The name of the effect

        :returns: True if successful, otherwise False
        """
        data = {"select": effect_name}
        r = requests.put(self.url + "/effects", data=json.dumps(data))
        return self.__error_check(r.status_code)

    def list_effects(self):
        """Returns a list of available effects"""
        r = requests.get(self.url + "/effects/effectsList")
        return json.loads(r.text)

    def effect_exists(self, effect_name):
        """Verifies whether an effect exists

        :param effect_name: Name of the effect to verify

        :returns: True if effect exists, otherwise False
        """
        r = requests.get(self.url + "/effects/effectsList")
        if effect in json.loads(r.text):
            return True
        return False

    #######################################################
    ####                  LAYOUT                       ####
    #######################################################

    def get_layout(self):
        """Returns the device layout information"""
        r = requests.get(self.url + "/panelLayout/layout")
        return json.loads(r.text)

    #######################################################
    ####                  EVENTS                       ####
    #######################################################

    def register_event(self, func, event_types):
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
        for e in event_types:
            if e < 1 or e > 4:
                raise Exception("Valid event types must be between 1-4")
        self.already_registered = True
        t = Thread(target=self.__event_listener, args=(func, event_types))
        t.start()

    def __event_listener(self, func, event_types):
        """Listens for events and passes event data to the user-defined
        function."""
        def inner():
            url = self.url + "/events?id="
            for e in event_types:
                url += str(e) + ","
            try:
                messages = SSEClient(url[:-1])
            except Exception as e:
                print("Events stream failed.")
                return inner()
            for msg in messages:
                func(json.loads(str(msg)))
        return inner()
