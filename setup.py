from setuptools import setup
import os

__local__ = os.path.abspath(os.path.dirname(__file__))
f_version = os.path.join(__local__, 'miniprez', '_version.py')
exec(open(f_version).read())

setup(
    name="miniprez",
    packages=['miniprez'],
    version=__version__,
    author="Travis Hoppe",
    author_email="travis.hoppe+miniprez@gmail.com",
    description=(
        "Simple markup to web-friendly presentations that look great on mobile and on the big screen."),
    license = "Creative Commons Attribution-ShareAlike 4.0 International License",
    keywords = ["presentations", "reveal.js", "powerpoint", ],
    url="https://github.com/thoppe/miniprez",
    test_suite="tests",
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'miniprez=miniprez.__main__:main',
        ]
    },
    
    install_requires=[
        "pyparsing",
        "bs4",
        "emoji",
        "lxml",
        "docopt",
    ],
    
    # Fill this in when ready...
    download_url='',
)
