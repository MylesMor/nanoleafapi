Getting Started
======================================

Installation
-----------------

To install run:

.. code-block::
    
    pip install nanoleafapi

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

.. code-block:: python

  from nanoleafapi import Nanoleaf

Next, a Nanoleaf object can be created with the following section of code. IF you don't have an authentication token yet, hold the power button for 5-7 seconds on your Nanoleaf device before running the following code. This will generate a new token and save it to your user directory to use for future uses of this package.

.. code-block:: python
  
  nl = Nanoleaf("ip")

You can now use the commands to control the panels as displayed in the example below.

.. code-block:: python

  nl.toggle_power()
  nl.set_color((255, 0, 0))            # Set colour to red

