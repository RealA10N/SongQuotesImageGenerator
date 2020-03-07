import click
import QuoteImageGenerator
import os

@click.command()

@click.option('--quote', '--quotes' ,'-q', prompt=True, required=True, multiple=True,
              type=str, help="Image quote.")

@click.option('--style', '-s', required=False, default="colored",
              type=click.Choice(["colored", "black"], case_sensitive=False),
              help="Image style.")

@click.option('--shuffle-styles', '--shuffle', required=False, is_flag=True,
              help="Each quote will get a different style.")

@click.option('--name', '-n', required=False, type=str, default="QuoteImage",
              help="Name of saved generated file.")

@click.option('--dir', '-d', required=False,
              type=click.Path(exists=False, writable=True, file_okay=False, dir_okay=True),
              help="Final image saving directory.")

@click.option('--save', required=False, type=bool, default=True,
              help="Save the generated image.")

@click.option('--show', required=False, type=bool, default=True,
              help="Open a popup with the generated image.")

def main(quote, style, shuffle_styles, name, dir, save, show):
    '''Generates image or a list of images from a given quote or quotes.'''

    for quote_index, cur_quote in enumerate(quote): 

        # selecting image style
        if style == "colored":
            if quote_index % 2 == 0 or not shuffle_styles:
                generator_class = QuoteImageGenerator.ColoredQuoteImage
            else:
                generator_class = QuoteImageGenerator.BlackQuoteImage
        elif style == "black":
            if quote_index % 2 == 0 or not shuffle_styles:
                generator_class = QuoteImageGenerator.BlackQuoteImage
            else:
                generator_class = QuoteImageGenerator.ColoredQuoteImage


        # generating image    
        generetor = generator_class(cur_quote)
        image = generetor.get_full_image()

        # saving generated image
        if save:
            if dir is None:
                dir = os.getcwd()
            
            if quote_index != 0:
                cur_name = name + str(quote_index + 1)

            image.save(os.path.join(dir, cur_name + ".png"))

        # showing image popup
        if show:
            image.show()