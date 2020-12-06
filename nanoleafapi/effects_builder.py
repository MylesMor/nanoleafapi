from PyInquirer import prompt, print_json
from prompt_toolkit.validation import Validator, ValidationError
import colorsys
import pprint



class Effect():

    def __init__(self, command, loop, anim_type):
        """Initialises the Effect class with the pre-answered questions.
        """
        self.command = command
        self.anim_type = anim_type
        self.effect = {
            "command": command, 
            "loop": loop, 
            "animType": anim_type, 
            "colorType": "HSB",
            "palette": None,
        }

    def set_name(self, name):
        """Sets the name field in the Effects dictionary.

        :param name: Animation name.
        """
        self.effect["animName"] = name

    def set_duration(self, duration):
        """Sets the duration field in the Effects dictionary.
        
        :param duration: Duration of the animation.
        """
        self.effect["duration"] = duration
        
    def set_animdata(self, anim_data):
        """Sets the animData field in the Effects dictionary.
        
        :param anim_data: Animation data.
        """
        self.effect["animData"] = anim_data

    def set_palette(self, palette):
        """Sets the palette (colour data) for the effect.

        :param: RGB colour string.
        """
        colour_list = []
        col_string = palette.replace(" ", "")
        colours = col_string.split(":")
        for colour in colours:
            rgb = colour.replace("(", "").replace(")", "").split(",")
            hsv_colour = colorsys.rgb_to_hsv(int(rgb[0])/255, int(rgb[1])/255, int(rgb[2])/255)
            hsv_colour = list(hsv_colour)
            hsv_colour[0] *= 360
            hsv_colour[1] *= 100
            hsv_colour[2] *= 100
            final_colour = [ int(x) for x in hsv_colour ]
            data = {
                "hue": final_colour[0],
                "saturation": final_colour[1],
                "brightness": final_colour[2]
            }
            colour_list.append(data)
        self.effect['palette'] = colour_list

    def print(self):
        """Prints the final Effects dictionary.
        """
        pprint.pprint(self.effect)


def interactive_builder():
    """Starts the interactive effects builder.
    """
    print("Welcome to the effects builder!")
    questions = [
        {
            'type': 'list',
            'name': 'command',
            'message': "Choose command type:",
            'choices': [
                'Display (temporary effect)',
                'Add (permanent effect)'
            ]
        },
        {
            'type': 'confirm',
            'name': 'loop',
            'message': "Should the effect loop?",
        },
        {
            'type': 'list',
            'name': 'animType',
            'message': "Choose animation type:",
            'choices': [
                'Random',
                'Flow',
                'Wheel',
                'Fade',
                'Highlight',
                'Custom',
                'Static',
            ]
        },
    ]
    answers = prompt(questions)
    effect = Effect(answers['command'].split(" (")[0].lower(), answers['loop'], answers['animType'].lower())
    questions = [
        {
            'type': 'input',
            'name': 'duration',
            'message': "Enter the duration of the effect in seconds (or 0 for forever): ",
            'validate': IntegerValidator
        },
        {
            'type': 'input',
            'name': 'palette',
            'message': "Enter RGB colours in the following format: (R,G,B):(R,G,B)",
            'validate': ColourValidator
        },
    ]
    extra_questions = check_for_extra_questions(effect)
    questions[:0] = extra_questions
    answers = prompt(questions)
    effect.set_duration(answers['duration'])
    effect.set_palette(answers['palette'])
    if "name" in answers:
        effect.set_name(answers['name'])
    if "animData" in answers:
        effect.set_animdata(answers['animData'])
    effect.print()
    
    

def check_for_extra_questions(effect):
    """Checks for extra questions that should be asked based on the animType.

    :param effect: The effect object.
    """
    questions = []
    if (effect.command == "add"):
        question = {
            'type': 'input',
            'name': 'name',
            'message': "Enter the name of the new effect:"
        }
        questions.insert(0, question)
    if effect.anim_type == "custom" or effect.anim_type == "static":
        question = {
            'type': 'input',
            'name': 'animData',
            'message': "Please enter the animation data: "
        }
        questions.insert(1, question) 
    return questions

class IntegerValidator(Validator):
    """Validates that the entered number is an integer.
    """
    def validate(self, document):
        try:
            duration = int(document.text)
            if (duration < 0):
                raise Exception()
        except:
            raise ValidationError(message='Please enter a valid positive integer.', cursor_position=len(document.text))

class ColourValidator(Validator):
    """Validates the RGB colour string.
    """
    def validate(self, document):
        col_string = document.text.replace(" ", "")
        colours = col_string.split(":")
        if (len(colours) == 0):
            raise ValidationError(message='Invalid colour string! Please follow the format specified and ensure colours are seperated by a colon.', cursor_position=len(document.text))
        for colour in colours:
            components = colour.replace("(", "").replace(")", "").split(",")
            if (len(components) != 3):
                raise ValidationError(message='Invalid colour string! Please follow the format specified and ensure colours are seperated by a colon.', cursor_position=len(document.text))
            for component in components:
                try:
                    comp_int = int(component)
                    if comp_int > 255 or comp_int < 0:
                        raise Exception()
                except:
                    raise ValidationError(message='Invalid colour string! Please ensure all RGB values are integers between 0 and 255.', cursor_position=len(document.text))

    

