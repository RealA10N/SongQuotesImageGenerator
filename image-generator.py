import json
import colorsys
import random


def load_config():
    # Uses json package

    with open("config.json") as config_file:
        config = json.load(config_file)
    
    return config


def generate_background_color(config=load_config()):
    # Uses random and colorsys packages

    # Generate a random color
    color = colorsys.hsv_to_rgb(
        random.random(),               # hue
        config["image"]["saturation"], # saturation
        config["image"]["lightness"])  # lightness, brightness

    # Convert to int from float
    color = list(color)
    for i, value in enumerate(color):
        color[i] = int(value)
    
    return tuple(color)
