from setuptools import setup

setup(
    name = "quoteimage",
    version = "1.0",
    
    install_requires = [
        "lyricsgenius", "Pillow", "click"
    ],

    py_modules = ["script", "QuoteImageGenerator", "TextImageGenerator", "BaseImageGenerator"],
    entry_points = {
        "console_scripts": [
            "quoteimage=script:main",
            "quoteimages=script:main"
        ]
    }
)