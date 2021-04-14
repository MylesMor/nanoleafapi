from typing import Tuple
from nanoleafapi.nanoleaf import NanoleafEffectCreationError, Nanoleaf

class NanoleafDigitalTwin():

    def __init__(self, nl : Nanoleaf):
        ids = nl.get_ids()
        self.nl = nl
        self.tile_dict = {}
        for panel_id in ids:
            self.tile_dict[panel_id] = {"R": 0, "G": 0, "B": 0, "W": 0, "T": 0}


    def set_color(self, panel_id : int, rgb : Tuple[int, int, int]):
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


    def get_ids(self):
        return list(self.tile_dict.keys())


    def get_color(self, panel_id : int):
        if panel_id not in self.tile_dict:
            raise NanoleafEffectCreationError("Invalid panel ID")
        return (self.tile_dict[panel_id]['R'], self.tile_dict[panel_id]['G'], self.tile_dict[panel_id]['B'])


    def get_all_colors(self):
        color_dict = {}
        for key, value in self.tile_dict.items():
            color_dict[key] = (value['R'], value['G'], value['B'])
        return color_dict

    def apply_changes(self):
        anim_data = str(len(self.tile_dict))
        for key, value in self.tile_dict.items():
            anim_data += " {key} {f} {r} {g} {b} {w} {t}".format(key=str(key), f=1, r=str(value['R']),  g=str(value['G']),  b=str(value['B']),  w=str(value['W']),  t=str(value['T']))
        base_effect = self.nl.get_custom_base_effect()
        base_effect['animData'] = anim_data
        return self.nl.write_effect(base_effect)