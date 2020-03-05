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
  nanoleaf_dict = discovery.discover_devices()

This will return a dictionary in the format: `{name: ip}`.


Usage
----------------------

There is just one class that contains all relevant functions for controlling the lights. To get started:

`from nanoleafapi import Nanoleaf`

Next, a Nanoleaf object can be created with:

`nl = Nanoleaf(ip)`

Next, if you don't have an authentication token, hold the power button on the lights for 5-7 seconds and then run:

`nl.generate_auth_token()`

__IMPORTANT__: Once this has been run, it will print your authentication token to the console. Please save this and in future runs of your program, initialise the Nanoleaf object with the authentication token:

`auth_token = XXXXXXXXXXXXXXXX`

`nl = nanoleaf(ip, auth_token)`
