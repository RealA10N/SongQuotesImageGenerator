from BaseImageGenerator import BaseImageGenerator
from PIL import Image, ImageDraw, ImageFont


class QuoteImageGenerator(BaseImageGenerator):

    def __init__(self):
        super().__init__()

        self._draw_image = ImageDraw.Draw(self.get_image())
        
        self._font = ImageFont.truetype(
            "fonts/Cocogoose-Classic-Medium.ttf",
            size = self._config["text"]["size"])
        
        self._max_text_width = self._max_text_width()

    
    def fancy_text(self, text):
        
        text = text.lower()

        text = text.replace("\r",". ")
        text = text.replace("\n",". ")

        text = " ".join(text.split())

        if text[-1] != ".":
            text += "."

        return text

    def draw_text(self, text):

        text = self.fancy_text(text)
        words = text.split()
        line_num = 0

        while words:
            
            max_index = len(words)

            while True:
                cur_line = ' '.join(words[:max_index])

                if self._draw_image.textsize(cur_line, self._font)[0] <= self._max_text_width or max_index == 1:
                    self._draw_line(cur_line, line_num)
                    words = words[max_index:]
                    break
                else:
                    max_index -= 1
            
            line_num += 1


    def _draw_line(self, text, line_num=0):
        
        x = self._config["text"]["padding"][0]
        y = self._config["text"]["padding"][1]
        y += line_num * (self._config["text"]["space-between-lines"] + self._config["text"]["size"]) 

        self._draw_image.text(
            (x, y),
            text,
            font=self._font,
            fill=self._config["text"]["color"])


    def _max_text_width(self):
        # Returns the maximum width of the text in each line

        width = self._config["image"]["size"][0]
        width -= 2 * self._config["text"]["padding"][0]
        width *= self._config["text"]["max-width-percentage"]
        return width
