"""NanoleafDigitalTwin

This module allows for the creation of a "digital twin", allowing you to make changes to individual panels and sync them to their real counterparts."""

from typing import Tuple, List, Dict
from nanoleafapi.nanoleaf import NanoleafEffectCreationError, Nanoleaf

class NanoleafDigitalTwin():
    """Class for creating and modifying digital twins

    :ivar nl: The Nanoleaf object
    :ivar tile_dict: The dictionary of tiles and their associated colour
    """

    def __init__(self, nl : Nanoleaf) -> None:
        """Initialises a digital twin based on the Nanoleaf object provided.

        :param nl: The Nanoleaf object 
        """
        ids = nl.get_ids()
        self.nl = nl
        self.tile_dict = {}
        for panel_id in ids:
            self.tile_dict[panel_id] = {"R": 0, "G": 0, "B": 0, "W": 0, "T": 0}


    def set_color(self, panel_id : int, rgb : Tuple[int, int, int]) -> None:
        """Sets the colour of an individual panel.

        :param panel_id: The ID of the panel to change the colour of
        :param rgb: A tuple containing the RGB values of the colour to set 
        """
        if panel_id not in self.tile_dict:
            raise NanoleafEffectCreationError("Invalid panel ID")
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
        self.tile_dict[panel_id]['R'] = rgb[0]
        self.tile_dict[panel_id]['G'] = rgb[1]
        self.tile_dict[panel_id]['B'] = rgb[2]


    def set_all_colors(self, rgb : Tuple[int, int, int]) -> None:
        """Sets the colour of all the panels.

        :param rgb: A tuple containing the RGB values of the colour to set 
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
        for key, value in self.tile_dict:
            self.tile_dict[key]['R'] = rgb[0]
            self.tile_dict[key]['G'] = rgb[1]
            self.tile_dict[key]['B'] = rgb[2]


    def get_ids(self) -> List[int]:
        """Returns a list of panel IDs.

        :returns: List of panel IDs.
        """
        return list(self.tile_dict.keys())


    def get_color(self, panel_id : int) -> Tuple[int, int, int]:
        """Returns the colour of a specified panel.

        :param panel_id: The panel to get the colour of.

        :returns: Returns the RGB tuple of the panel with ID panel_id.
        """
        if panel_id not in self.tile_dict:
            raise NanoleafEffectCreationError("Invalid panel ID")
        return (self.tile_dict[panel_id]['R'], self.tile_dict[panel_id]['G'], self.tile_dict[panel_id]['B'])


    def get_all_colors(self) -> Dict[int, Tuple(int, int, int)]:
        """Returns a dictionary of all panel IDs and associated colours.

        :returns: Dictionary with panel IDs as keys and RGB tuples as values.
        """
        color_dict = {}
        for key, value in self.tile_dict.items():
            color_dict[key] = (value['R'], value['G'], value['B'])
        return color_dict

    def sync(self) -> bool:
        """Syncs the digital twin's changes to the real Nanoleaf device.

        :returns: True if success, otherwise False
        """
        anim_data = str(len(self.tile_dict))
        for key, value in self.tile_dict.items():
            anim_data += " {key} {f} {r} {g} {b} {w} {t}".format(key=str(key), f=1, r=str(value['R']),  
                g=str(value['G']),  b=str(value['B']),  w=str(value['W']),  t=str(value['T']))
        base_effect = self.nl.get_custom_base_effect()
        base_effect['animData'] = anim_data
        return self.nl.write_effect(base_effect)