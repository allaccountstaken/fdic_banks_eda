from distutils.core import setup
from ffipy import __version__

setup(name='ffipy',
      version=__version__,
      description='Tools for retrieving data from the FFIEC SOAP servers.',
      author='Ryan Arredondo',
      author_email='ryan.c.arredondo@gmail.com',
      url='https://github.com/rarredon/ffipy/',
      packages=['ffipy']
)
