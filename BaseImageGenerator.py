import json
import colorsys
from PIL import Image
import random


class BaseImageGenerator:

    def __init__(self):      

        _base_image = None

        with open("config.json") as config_file:
            self._config = json.load(config_file)
    

    def get_background_color(self, hue):

        if not isinstance(hue, int):
            hue = random.random()

        color = colorsys.hsv_to_rgb(
            hue,                                 # hue
            self._config["image"]["saturation"], # saturation
            self._config["image"]["lightness"])  # lightness, brightness

        # Convert to int from float
        color = list(color)
        for i, value in enumerate(color):
            color[i] = int(value)
        
        return tuple(color)


    # BASE IMAGE

    def get_base_image(self, hue=None):
        
        if hue is not None or self._base_image is None:
        # if given a custom hue or image is not generated yet
            self._generate_base_image(hue)
        
        return self._base_image


    def _generate_base_image(self, hue):
        self._base_image = Image.new(
            mode = "RGB",
            size = self._config["image"]["size"],
            color = self.get_background_color(hue))
