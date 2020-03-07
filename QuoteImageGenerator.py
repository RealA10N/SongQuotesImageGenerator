from TextImageGenerator import _BasicTextImage, ColoredTextImage, BlackTextImage
from PIL import Image, ImageDraw, ImageFont
import lyricsgenius


class _BasicQuoteImage(_BasicTextImage):

    def __init__(self, text):
        super().__init__(text)

        self.text = text

        genius = lyricsgenius.Genius(self._config["api"]["client-access-token"], verbose=False)
        song = genius.search_song(self.text)        
        self.desc = '"' + song.title + '" by ' + song.artist

        self._desc_font = ImageFont.truetype(
            self._config[self._version]["desc-text"]["font-path"],
            size = self._config[self._version]["desc-text"]["size"])

    def get_full_image(self):
        self.add_text(self.text)
        self.add_credit()
        return self.get_image()


class BlackQuoteImage(_BasicQuoteImage, BlackTextImage):

    def add_credit(self):
        starting_y = self._config[self._version]["image"]["size"][1]
        starting_y += self._text_height
        starting_y /= 2
        starting_y += self._config[self._version]["text"]["padding"][1]

        starting_x = self._config[self._version]["image"]["size"][0] - self._draw_image.textsize(self.desc, self._desc_font)[0]
        starting_x /= 2

        self._draw_image.text(
            (int(starting_x), int(starting_y)),
            self.desc,
            font=self._desc_font,
            fill=self._config[self._version]["desc-text"]["color"])

