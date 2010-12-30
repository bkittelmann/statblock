from distutils.core import setup

setup(
    name='statblock',
    version='0.1dev',
    author='Benno Kittelmann',
    url='https://github.com/bkittelmann/statblock',
    packages=['statblock', 'statblock.transform'],
    requires=["lxml"],
    license="BSD",
    long_description=open('README.txt').read(),
)
