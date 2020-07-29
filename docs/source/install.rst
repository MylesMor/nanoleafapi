Getting Started
======================================

Installation
-----------------

To install run:

``pip install nanoleafapi``

Prerequisites
----------------

You must know the IP address of the Nanoleaf device. This can be either be done using your own methods or by using the disovery module. This module uses SSDP and should work __but__ I have found cases of this method not functioning properly. If it doesn't work, and gives an empty dictionary please identify the IP of the Nanoleaf device yourself.

To use the discovery module:

.. code-block:: python

  from nanoleafapi import discovery
  nanoleaf_dict = discovery.discover_devices(timeout=30)

This will return a dictionary in the format: ``{name: ip}``.


Usage
----------------------

There is just one class that contains all relevant functions for controlling the lights. To get started:

``from nanoleafapi import Nanoleaf``

Next, a Nanoleaf object can be created with:

``nl = Nanoleaf(ip)``

Next, if you don't have an authentication token, hold the power button on the lights for 5-7 seconds and then run:

``nl.generate_auth_token()``

__IMPORTANT__: Once this has been run, it will print your authentication token to the console. Please save this and in future runs of your program, initialise the Nanoleaf object with the authentication token:

``auth_token = XXXXXXXXXXXXXXXX``

``nl = nanoleaf(ip, auth_token)``


Methods
-------------------

All of the following methods can be called with the Nanoleaf object you created.

For more information about the Nanoleaf API: https://forum.nanoleaf.me/docs/openapi

For more in-depth documentation about this package visit: https://nanoleafapi.readthedocs.io/en/latest/api.html

User Management
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

  generate_auth_token()     # Generates new authentication token (hold power for 5-7 before running)
  delete_user(auth_token)   # Deletes an authentication token from the device


Power
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

  get_power()               # Returns True if lights are on, otherwise False
  power_off()               # Powers off the lights
  power_on()                # Powers on the lights
  toggle_power()            # Toggles light on/off


Colour
~~~~~~~~~~~~~~~~~~~~~~

Colours are generated using HSV (or HSB) in the API, and these individual values can be adjusted using methods which are as described, hue, brightness and saturation. The method in this section uses RGB (0-255) and converts this to HSV.

There are already some pre-set colours which can be imported to be used with the ``set_color()`` method:

.. code-block:: python

  from nanoleafapi import RED, ORANGE, YELLOW, GREEN, LIGHT_BLUE, BLUE, PINK, PURPLE, WHITE


The ``set_color()`` method can then be called, passing in either a pre-set colour or your own RGB colour in the form of a tuple: ``(r, g, b)``.

.. code-block:: python

  set_color((r, g, b))      # Set all lights to RGB colour. Pass the colour as a tuple.
  set_color(RED)            # Same result but using a pre-set colour.

Brightness
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

  set_brightness(brightness, duration)     # Sets the brightness of the lights (accepts values between 0-100)
  increment_brightness(value)              # Increments the brightness by set amount (can also be negative)
  get_brightness()                         # Returns current brightness


Hue
~~~~~~~~~~~~~~~~~~~~~~

Use these if you want to change the HSV values manually, otherwise use ``set_color()`` for colour change using RGB.

.. code-block:: python

  set_hue(value)            # Sets the hue of the lights (accepts values between 0-360)
  increment_hue(value)      # Increments the hue by set amount (can also be negative)
  get_hue()                 # Returns current hue


Saturation
~~~~~~~~~~~~~~~~~~~~~~

Use these if you want to change the HSV values manually, otherwise use ``set_color()`` for colour change using RGB.

.. code-block:: python

  set_saturation(value)            # Sets the saturation of the lights (accepts value between 0-100)
  increment_saturation(value)      # Increments the saturation by set amount (can also be negative)
  get_saturation()                 # Returns current saturation


Identify
~~~~~~~~~~~~~~~~~~~~~~

This is usually used to identify the current lights by flashing them on and off.

.. code-block:: python

  identify()


Colour Temperature
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

  set_color_temp(value)            # Sets the colour temperature of the lights (accepts between 1200-6500)
  increment_color_temp(value)      # Increments the colour temperature by set amount (can also be negative)
  get_color_temp()                 # Returns current colour temperature


Colour Mode
~~~~~~~~~~~~~~~~~~~~~~

Not really sure what this is for, but included it anyway.

.. code-block:: python

  get_color_mode()      # Returns current colour mode


Effects
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

  get_current_effect()    # Returns either name of current effect if available or *Solid*/*Static*/*Dynamic*.
  list_effects()          # Returns a list of names of all available effects.
  effect_exists(name)     # Helper method which determines whether the given string exists as an effect.
  set_effect(name)        # Sets the current effect.

Write Effect
~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: python

  write_effect(effect_dict)    # Sets a user-created effect.

Writing effects is rather complicated; you need to follow the the exact format for the effect dictionary, which can be found here: https://forum.nanoleaf.me/docs/openapi#_u2t4jzmkp8nt

In future updates, I hope to add a way to make this process easier, but for now an example of a valid effect dictionary is provided below:

.. code-block:: python

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
  

Inputting an invalid dictionary will result in the function returning False, and it printing to the console `Invalid effect dictionary!`.


Events
~~~~~~~~~~~~~~~~~~~~~~
Creates an event listener for the different types of events.

.. code-block:: python

  register_event(function, event_types)

You should pass your own function with one argument (event as a dictionary). This function will run every time a new event is received.

**IMPORTANT**: You cannot currently call ``register_event()`` more than **once** due to API limitations. Instead, distinguish between the events in your function using the dictionary data.

A list of event types you would like to listen for should also be passed. You can register up to 4 events (all of them), and these are listed below:

Event IDs:

| State (changes in power/brightness): **1**
| Layout: **2**
| Effects: **3**
| Touch (canvas only): **4**


Example Usage
++++++++++++++++

.. code-block:: python

  def event_function(event):
      print(event)

  # Register for all events
  nl.register_event(event_function, [1, 2, 3, 4])


Example Output
++++++++++++++++

When an event occurs, the ``event_function()`` will run and therefore in this case, print the event dictionary.

.. code-block:: python

  {"events":[{"attr":2,"value":65}]}                 # Example of state event (1)
  {"events":[{"attr":1,"value":"Falling Whites"}]}   # Example of effects event (3)
  {"events":[{"panelId":7397,"gesture":0}]}          # Example of touch event (4)
