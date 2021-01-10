# nanoleafapi

[![PyPI version](https://badge.fury.io/py/nanoleafapi.svg)](https://badge.fury.io/py/nanoleafapi) [![Documentation Status](https://readthedocs.org/projects/nanoleafapi/badge/?version=latest)](https://nanoleafapi.readthedocs.io/en/latest/?badge=latest) [![Downloads](https://pepy.tech/badge/nanoleafapi)](https://pepy.tech/project/nanoleafapi)


__nanoleafapi__ is a Python 3 wrapper for the Nanoleaf OpenAPI. It provides an easy way to use many of the functions available in the API. It supports the Light Panels (previously Aurora), Canvas and Shapes (including Hexgaons).

__Nanoleaf API__: https://forum.nanoleaf.me/docs/openapi

__Detailed package documentation__: https://nanoleafapi.readthedocs.io

__IMPORTANT__: As of version 2.0.0, there have been some API changes relating to how the authentication token is generated and stored, please re-read the [Usage](#Usage) section.

# Table of Contents
1. [Installation](#Installation)
2. [Prerequisites](#Prerequisites)
3. [Usage](#Usage)
   * [Methods](#Methods)
   * [Effects](#Effects)
   * [Events](#Events)
   * [Errors](#Errors)
4. [Upcoming Features](#Upcoming-Features)

## Installation
To install the latest stable release:

```batch
python -m pip install nanoleafapi
```

## Prerequisites

You must know the IP address of the Nanoleaf device. This can be either be done using your own methods or by using the disovery module. This module uses SSDP and should work __but__ I have found cases of this method not functioning properly. If it doesn't work, and gives an empty dictionary please identify the IP of the Nanoleaf device yourself.

To use the discovery module:

```py
from nanoleafapi import discovery

nanoleaf_dict = discovery.discover_devices()
```

This will return a dictionary in the format: `{name: ip}`.


## Usage

There is just one class that contains all relevant functions for controlling the lights. To get started:

```py 
from nanoleafapi import Nanoleaf
```

Next, a Nanoleaf object can be created with the following line of code. __IF you don't have an authentication token yet, hold the power button for 5-7 seconds on your Nanoleaf device before running the following code. This will generate a new token and save it to your user directory to use for future uses of this package.__

```py 
nl = Nanoleaf("ip")
```

You can now use the commands to control the panels as displayed in the example below.

```py
nl.toggle_power()             # Toggle power
nl.set_color((255, 0, 0))     # Set colour to red
```

![Example setup](https://github.com/MylesMor/nanoleafapi/blob/master/photos/nanoleafapi_new_example.png?raw=true)

## Methods

All of the following methods can be called with the Nanoleaf object you created.

For more information about the Nanoleaf API: https://forum.nanoleaf.me/docs/openapi

For more in-depth documentation about this package visit: https://nanoleafapi.readthedocs.io

#### User Management
```py
delete_auth_token(auth_token)   # Deletes an authentication token from the device and the token storage file.
```

#### General
```py
get_info()         # Returns device information dictionary
get_name()         # Returns the current device name
check_connection() # Raises NanoleafConnectionError if connection fails
```

#### Power
```py
get_power()               # Returns True if lights are on, otherwise False
power_off()               # Powers off the lights
power_on()                # Powers on the lights
toggle_power()            # Toggles light on/off
```

#### Colour
Colours are generated using HSV (or HSB) in the API, and these individual values can be adjusted using methods which are as described, [hue](#Hue), [saturation](#Saturation), [brightness/value](#Brightness). The method in this section uses RGB (0-255) and converts this to HSV.

There are already some pre-set colours which can be imported to be used with the ``set_color()`` method:

```py
from nanoleafapi import RED, ORANGE, YELLOW, GREEN, LIGHT_BLUE, BLUE, PINK, PURPLE, WHITE
```

The `set_color()` method can then be called, passing in either a pre-set colour or your own RGB colour in the form of a tuple: `(r, g, b)`.

```py
set_color((r, g, b))      # Set all lights to RGB colour. Pass the colour as a tuple.
set_color(RED)            # Same result but using a pre-set colour.
```

#### Brightness
```py
set_brightness(brightness, duration)     # Sets the brightness of the lights (accepts values between 0-100)
increment_brightness(value)              # Increments the brightness by set amount (can also be negative)
get_brightness()                         # Returns current brightness
```

#### Hue
Use these if you want to change the HSV values manually, otherwise use `set_color()` for colour change using RGB.
```py
set_hue(value)            # Sets the hue of the lights (accepts values between 0-360)
increment_hue(value)      # Increments the hue by set amount (can also be negative)
get_hue()                 # Returns current hue
```

#### Saturation
Use these if you want to change the HSV values manually, otherwise use `set_color()` for colour change using RGB.

```py
set_saturation(value)            # Sets the saturation of the lights (accepts value between 0-100)
increment_saturation(value)      # Increments the saturation by set amount (can also be negative)
get_saturation()                 # Returns current saturation
```

#### Identify
This is usually used to identify the current lights by flashing them on and off.
```py
identify()
```

#### Colour Temperature
```py
set_color_temp(value)            # Sets the colour temperature of the lights (accepts between 1200-6500)
increment_color_temp(value)      # Increments the colour temperature by set amount (can also be negative)
get_color_temp()                 # Returns current colour temperature
```

#### Colour Mode
Not really sure what this is for, but included it anyway.
```py
get_color_mode()      # Returns current colour mode
```

### Effects
```py
get_current_effect()    # Returns either name of current effect if available or *Solid*/*Static*/*Dynamic*.
list_effects()          # Returns a list of names of all available effects.
effect_exists(name)     # Helper method which determines whether the given string exists as an effect.
set_effect(name)        # Sets the current effect.
```

#### Custom Effects
```py
pulsate(rgb_tuple, speed)     # Displays a pulsate effect with the specified colour and speed.
flow(rgb_tuple_list, speed)   # Displays a sequence of specified colours and speed.
spectrum(speed)               # Displays a spectrum cycling effect with the specified speed.
```

#### Write Effect
```py
write_effect(effect_dict)    # Sets a user-created effect.
```
Writing effects is rather complicated; you need to follow the the exact format for the effect dictionary, which can be found here: https://forum.nanoleaf.me/docs/openapi#_u2t4jzmkp8nt

In future updates, I hope to add a way to make this process easier, but for now an example of a valid effect dictionary is provided below:

```py
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
                    "hue": 180,
                    "saturation": 100,
                    "brightness": 100
                }
            ],
            "brightnessRange": {
                "minValue": 50,
                "maxValue": 100
            },
            "transTime": {
                "minValue": 50,
                "maxValue": 100
            },
            "delayTime": {
                "minValue": 50,
                "maxValue": 100
            },
            "loop": True
        }
```

Inputting an invalid dictionary will result in the function returning False, and it printing to the console `Invalid effect dictionary!`.

### Events
Creates an event listener for the different types of events.

```py
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
Touch (Canvas/Shapes only): 4
```

#### Example Usage

```py
def event_function(event):
    print(event)

# Register for all events
nl.register_event(event_function, [1, 2, 3, 4])
```

#### Example Output

When an event occurs, the `event_function()` will run and therefore in this case, print the event dictionary.

```py
{"events":[{"attr":2,"value":65}]}                 # Example of state event (1)
{"events":[{"attr":1,"value":"Falling Whites"}]}   # Example of effects event (3)
{"events":[{"panelId":7397,"gesture":0}]}          # Example of touch event (4)
```

### Errors
```py
NanoleafRegistrationError()  # Raised when token generation mode not active on device
NanoleafConnectionError()    # Raised when there is a connection error during check_connection() method
```

## Upcoming Features
Currently in development is an CLI effects builder, to help with the `write_effect` functionality. This will allow you to quickly and easily create the dictionaries required to make your own effects!

Here's a sneak peek:

![Effects builder](https://github.com/MylesMor/nanoleafapi/blob/master/photos/effects-builder.png?raw=true)
