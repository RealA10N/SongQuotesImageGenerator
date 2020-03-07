from TextImageGenerator import _BasicTextImage, ColoredTextImage, BlackTextImage
from PIL import Image, ImageDraw, ImageFont
import lyricsgenius
import requests
from io import BytesIO


class _BasicQuoteImage(_BasicTextImage):

    def __init__(self, text):
        super().__init__(text)

        genius = lyricsgenius.Genius(self._config["api"]["client-access-token"], verbose=False)
        song = genius.search_song(self.text)        
        self.desc = '"' + song.title + '" by ' + song.artist
        self.art_image_url = song.song_art_image_url

        self._desc_font = ImageFont.truetype(
            self._config[self._version]["desc"]["font-path"],
            size = self._config[self._version]["desc"]["size"])

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
            fill=self._config[self._version]["desc"]["color"])


class ColoredQuoteImage(_BasicQuoteImage, ColoredTextImage):

    def add_credit(self):
        
        self.pasting_song_art_image()


    def _pasting_song_art_image(self):
        # getting image
        response = requests.get(self.art_image_url)
        art_image = Image.open(BytesIO(response.content))

        # resizing image
        image_size = (self._config[self._version]["desc"]["size"] * 2) + self._config[self._version]["desc"]["space-between-lines"]
        art_image = art_image.resize((image_size, image_size))

        # calculating pasting position
        starting_x = self._config[self._version]["image"]["size"][0] - self._config[self._version]["text"]["padding"][0] - image_size
        starting_y = self._config[self._version]["image"]["size"][1] - self._config[self._version]["text"]["padding"][1] - image_size

        # shadow
        self._draw_image.rectangle(
            [(starting_x, starting_y),
            (starting_x + image_size, starting_y + image_size)],
            fill=self._config[self._version]["desc"]["shadow-color"])

        # pasting art image
        starting_x -= self._config[self._version]["desc"]["shadow-size"][0]
        starting_y -= self._config[self._version]["desc"]["shadow-size"][1]
        self.get_image().paste(art_image, (starting_x, starting_y))



