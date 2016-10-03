from distutils.core import setup

setup(name='hullpy',
      version='0.1.0',
      descriptions='Hull Python library',
      long_description=__doc__,
      author="ByoungYong Kim",
      author_email="byoungyong@sense-os.nl",
      py_modules=['hull'],
      install_requires=['requests'])
