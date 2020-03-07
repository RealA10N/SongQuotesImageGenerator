from BaseImageGenerator import ColoredBaseImage, BlackBaseImage
from PIL import Image, ImageDraw, ImageFont



class _BasicTextImage(ColoredBaseImage):

    def __init__(self, text):
        super().__init__()

        self._draw_image = ImageDraw.Draw(self.get_image())
        self.text = text

        self._font = ImageFont.truetype(
            self._config[self._version]["text"]["font-path"],
            size = self._config[self._version]["text"]["size"])
        
        self._max_text_width = self._max_text_width()

    def fancy_text(self, text):
    
        text = text.lower()              # makes all lowercase

        text = text.replace("\r"," ")   # remove new lines
        text = text.replace("\n"," ")

        text = " ".join(text.split())    # remove whitespaces

        if text[0] != '"':               # add " (quotes) and . (dots)
            text = '"' + text
        if text[-1] != '"' and text[-2] != '"':
            text += '"'
        if text[-2] != "." and text[-2] != "?" and text[-2] != "!":
            text = text[:-1] + '."'

        return text

    def split_text_to_lines(self, text):

        text = self.fancy_text(text)
        words = text.split()
        line_num = 0

        lines = []

        while words:
            
            max_index = len(words)

            while True:
                cur_line = ' '.join(words[:max_index])

                if self._draw_image.textsize(cur_line, self._font)[0] <= self._max_text_width or max_index == 1:
                    lines.append(cur_line)
                    words = words[max_index:]
                    break
                else:
                    max_index -= 1
            
            line_num += 1
        
        return lines
    
    def _max_text_width(self):
        width = self._config[self._version]["image"]["size"][0]
        width -= 2 * self._config[self._version]["text"]["padding"][0]
        width *= self._config[self._version]["text"]["max-width-percentage"]
        return width



class ColoredTextImage(_BasicTextImage, ColoredBaseImage):

    def __init__(self):
        super().__init__()


    def _draw_line(self, text, line_num=0):
        
        x = self._config[self._version]["text"]["padding"][0]
        y = self._config[self._version]["text"]["padding"][0]
        y += line_num * (self._config[self._version]["text"]["space-between-lines"] + self._config[self._version]["text"]["size"]) 

        self._draw_image.text(
            (x, y),
            text,
            font=self._font,
            fill=self._config[self._version]["text"]["color"])


    def add_text(self, text):
        lines = self.split_text_to_lines(text)

        for line_num, line in enumerate(lines):
            self._draw_line(line, line_num=line_num)



class BlackTextImage(_BasicTextImage, BlackBaseImage):
    
    _text_height = 0

    def add_text(self, text):
        lines = self.split_text_to_lines(text)

        self._text_height = len(lines) * (self._config[self._version]["text"]["space-between-lines"] + self._config[self._version]["text"]["size"])
        if len(lines) > 0:
            self._text_height -= self._config[self._version]["text"]["space-between-lines"]


        y = self._config[self._version]["image"]["size"][1] - self._text_height
        y /= 2

        if len(lines) > 0:
            y -= self._config[self._version]["text"]["space-between-lines"]
        
        for line_num, line in enumerate(lines):
            self._draw_line(line, y, line_num=line_num,)


    def _draw_line(self, text, y, line_num=0):
        
        x = self._config[self._version]["image"]["size"][0] - self._draw_image.textsize(text, self._font)[0]
        x /= 2

        y += line_num * (self._config[self._version]["text"]["space-between-lines"] + self._config[self._version]["text"]["size"]) 

        self._draw_image.text(
            (x, y),
            text,
            font=self._font,
            fill=self._config[self._version]["text"]["color"])
