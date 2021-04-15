NanoleafDigitalTwin Methods
==================================

This class is used to make a digital twin (or copy) of the Nanoleaf device, allowing you to change the colour of individual tiles and then sync all the changes
at once to the real device.

To create an instance of this class, you must initialise it with a Nanoleaf object:

.. code-block:: python

    from nanoleafapi import Nanoleaf, NanoleafDigitalTwin

    nl = Nanoleaf("192.168.0.2")
    digital_twin = NanoleafDigitalTwin(nl)


Utility
----------------

.. code-block:: python

    get_ids()       # Returns a list of panel IDs


Colour
----------------
Setting the colour is all managed by using an RGB tuple, in the format: ``(R, G, B)``.

.. code-block:: python

    set_color(panel_id, (255, 255, 255))   # Sets the panel with specified ID to white
    set_all_colors((255, 255, 255))        # Sets all panels to white
    get_color(panel_id)                    # Gets the colour of a specified panel
    get_all_colors()                       # Returns a dictionary of {panel_id: (R, G, B)}


Sync
-----------------
The sync method applies the changes to the real Nanoleaf device, based on the changes made here.

.. code-block:: python

    sync()    # Syncs with the real Nanoleaf counterpart
