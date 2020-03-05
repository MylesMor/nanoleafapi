# nanoleafapi

[![PyPI version](https://badge.fury.io/py/nanoleafapi.svg)](https://badge.fury.io/py/nanoleafapi) [![Documentation Status](https://readthedocs.org/projects/nanoleafapi/badge/?version=latest)](https://nanoleafapi.readthedocs.io/en/latest/?badge=latest)


__nanoleafapi__ is a Python 3 wrapper for the Nanoleaf OpenAPI. It provides an easy way to use many of the functions available in the API. It supports both the Light Panels (previously Aurora) and Canvas.

__Nanoleaf API__: https://forum.nanoleaf.me/docs/openapi

__Detailed package documentation__: https://nanoleafapi.readthedocs.io

## Updates

__Current version__: `1.1.0`

__31/12/19__: As of package version `1.0.2`, the issue regarding not installing the correct dependencies has been fixed. Please upgrade your version with `pip install nanoleafapi --upgrade`.

__01/01/20__: As of package version `1.0.3`, there is now a connection check to determine whether the given IP is a valid Nanoleaf device. An exception will be raised if it is not found.

__05/01/20__: As of package version `1.0.5`, the bug described in issue #1 by [vadichi](https://github.com/vadichi) relating to the function `set_effect()` has been resolved.

__13/01/20__: As of package version `1.1.0`, added a discovery module to identify Nanoleaf devices on your network and a test class. To use this test class, please insert the IP of your Nanoleaf device and the authorisation token into `test_nanoleaf.py` in the `setUpClass` method.

# Table of Contents
1. [Installation](#Installation)
2. [Prerequisites](#Prerequisites)
3. [Usage](#Usage)
   * [Methods](#Methods)
   * [Effects](#Effects)
   * [Events](#Events)

## Installation
To install the latest stable release:

`pip install nanoleafapi`

## Prerequisites

You must know the IP address of the Nanoleaf device. This can be either be done using your own methods or by using the disovery module. This module uses SSDP and should work __but__ I have found cases of this method not functioning properly. If it doesn't work, and gives an empty dictionary please identify the IP of the Nanoleaf device yourself.

To use the discovery module:

```
from nanoleafapi import discovery

nanoleaf_dict = discovery.discover_devices()
```

This will return a dictionary in the format: `{name: ip}`.


## Usage

There is just one class that contains all relevant functions for controlling the lights. To get started:

`from nanoleafapi import Nanoleaf`

Next, a Nanoleaf object can be created with:

`nl = Nanoleaf(ip)`

Next, if you don't have an authentication token, hold the power button on the lights for 5-7 seconds and then run:

`nl.generate_auth_token()`

__IMPORTANT__: Once this has been run, it will print your authentication token to the console. Please save this and in future runs of your program, initialise the Nanoleaf object with the authentication token:

`auth_token = XXXXXXXXXXXXXXXX`

`nl = nanoleaf(ip, auth_token)`

## Methods

All of the following methods can be called with the Nanoleaf object you created.

For more information about the Nanoleaf API: https://forum.nanoleaf.me/docs/openapi

For more in-depth documentation about this package visit: https://nanoleafapi.readthedocs.io

#### User Management
```
generate_auth_token()     # Generates new authentication token (hold power for 5-7 before running)
delete_user(auth_token)   # Deletes an authentication token from the device
```

#### Power
```
get_power()               # Returns True if lights are on, otherwise False
power_off()               # Powers off the lights
power_on()                # Powers on the lights
toggle_power()            # Toggles light on/off
```

#### Colour
Colours are generated using HSV (or HSB) in the API, and these individual values can be adjusted using methods which are as described, [hue](#Hue), [saturation](#Saturation), [brightness/value](#Brightness). The method in this section uses RGB (0-255) and converts this to HSV.

There are already some pre-set colours which can be imported to be used with the ``set_color()`` method:

```
from nanoleafapi import RED, ORANGE, YELLOW, GREEN, LIGHT_BLUE, BLUE, PINK, PURPLE, WHITE
```

The `set_color()` method can then be called, passing in either a pre-set colour or your own RGB colour in the form of a tuple: `(r, g, b)`.

```
set_color((r, g, b))      # Set all lights to RGB colour. Pass the colour as a tuple.
set_color(RED)            # Same result but using a pre-set colour.
```

#### Brightness
```
set_brightness(brightness, duration)     # Sets the brightness of the lights (accepts values between 0-100)
increment_brightness(value)              # Increments the brightness by set amount (can also be negative)
get_brightness()                         # Returns current brightness
```

#### Hue
Use these if you want to change the HSV values manually, otherwise use `set_color()` for colour change using RGB.
```
set_hue(value)            # Sets the hue of the lights (accepts values between 0-360)
increment_hue(value)      # Increments the hue by set amount (can also be negative)
get_hue()                 # Returns current hue
```

#### Saturation
Use these if you want to change the HSV values manually, otherwise use `set_color()` for colour change using RGB.

```
set_saturation(value)            # Sets the saturation of the lights (accepts value between 0-100)
increment_saturation(value)      # Increments the saturation by set amount (can also be negative)
get_saturation()                 # Returns current saturation
```

#### Identify
This is usually used to identify the current lights by flashing them on and off.
```
identify()
```

#### Colour Temperature
```
set_color_temp(value)            # Sets the colour temperature of the lights (accepts between 1200-6500)
increment_color_temp(value)      # Increments the colour temperature by set amount (can also be negative)
get_color_temp()                 # Returns current colour temperature
```

#### Colour Mode
Not really sure what this is for, but included it anyway.
```
get_color_mode()      # Returns current colour mode
```

### Effects
```
get_current_effect()    # Returns either name of current effect if available or *Solid*/*Static*/*Dynamic*.
list_effects()          # Returns a list of names of all available effects.
effect_exists(name)     # Helper method which determines whether the given string exists as an effect.
set_effect(name)        # Sets the current effect.
```

### Events
Creates an event listener for the different types of events.

```
register_event(function, event_types)
```
You should pass your own function with one argument (event as a dictionary). This function will run every time a new event is received.

__IMPORTANT__: You cannot currently call ```register_event()``` more than __once__ due to API limitations. Instead, distinguish between the events in your function using the dictionary data.

A list of event types you would like to listen for should also be passed. You can register up to 4 events (all of them), and these are listed below:

Event IDs:
```
State (changes in power/brightness): 1
Layout: 2
Effects: 3
Touch (canvas only): 4
```

#### Example Usage

```
def event_function(event):
    print(event)

# Register for all events
nl.register_event(event_function, [1, 2, 3, 4])
```

#### Example Output

When an event occurs, the `event_function()` will run and therefore in this case, print the event dictionary.

```
{"events":[{"attr":2,"value":65}]}                 # Example of state event (1)
{"events":[{"attr":1,"value":"Falling Whites"}]}   # Example of effects event (3)
{"events":[{"panelId":7397,"gesture":0}]}          # Example of touch event (4)
```
