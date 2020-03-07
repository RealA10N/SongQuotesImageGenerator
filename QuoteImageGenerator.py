from TextImageGenerator import TextImageGenerator
from PIL import Image, ImageDraw, ImageFont


class QuoteImageGenerator(TextImageGenerator):

    def __init__(self, text):
        super().__init__()

    def fancy_text(self, text):
    
        text = text.lower()              # makes all lowercase

        text = text.replace("\r",". ")   # remove new lines
        text = text.replace("\n",". ")

        text = " ".join(text.split())    # remove whitespaces

        if text[0] != '"':               # add " (quotes) and . (dots)
            text = '"' + text
        if text[-1] != '"' and text[-2] != '"':
            text += '"'
        if text[-2] != ".":
            text = text[:-2] + '."'

        return text