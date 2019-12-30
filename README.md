# nanoleafapi
__nanoleafapi__ is a Python 3 wrapper for controlling the Nanoleaf OpenAPI. It supports both the Light Panels (previous Aurora) and Canvas.

## Installation
To install the latest stable release:

`pip install nanoleafapi`

## Prerequisites

You must know the IP address of the Nanoleaf device. This can be found by using `arp -a` and searching for your Nanoleaf MAC address or looking at connected devices on your router among other methods.

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
There are already some pre-set colours which can be imported:

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
set_brightness()
```
