import json
import colorsys
from PIL import Image
import random


class ColoredBaseImage:

    def __init__(self):      

        self._image = None
        self._version = "colored-version"

        with open("config.json") as config_file:
            self._config = json.load(config_file)
    

    def get_background_color(self, hue):

        if not isinstance(hue, int):
            hue = random.random()

        color = colorsys.hsv_to_rgb(
            hue,                                                # hue
            self._config[self._version]["image"]["saturation"], # saturation
            self._config[self._version]["image"]["lightness"])  # lightness, brightness

        # Convert to int from float
        color = list(color)
        for i, value in enumerate(color):
            color[i] = int(value)
        
        return tuple(color)


    # BASE IMAGE

    def get_image(self, hue=None):
        
        if hue is not None or self._image is None:
        # if given a custom hue or image is not generated yet
            self._generate_image(hue)
        
        return self._image


    def _generate_image(self, hue):
        self._image = Image.new(
            mode = "RGB",
            size = self._config[self._version]["image"]["size"],
            color = self.get_background_color(hue))


class BlackBaseImage(ColoredBaseImage):
    
    def __init__(self):
        super().__init__()
        self._version = "black-version"


    def get_background_color(self, *args):
        return self._config[self._version]["image"]["color"]

if __name__ == "__main__":
    y = BlackBaseImage()
    y.get_image().show()