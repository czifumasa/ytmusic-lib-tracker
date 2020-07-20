from setuptools import setup

setup(
    name='ytmusiclibtracer',
    url='https://github.com/czifumasa/ytmusic-lib-tracker',
    author='Łukasz Lenart',
    author_email='lukasz.lenart912@gmail.com',
    packages=['ytmusiclibtracker'],
    install_requires=['ytmusicapi', 'unidecode'],
    version='0.1',
    license='MIT',
    description='Useful tools for youtube music. Exporting library to csv, tracking changes in library, summary of transfer from GPM',
    # We will also need a readme eventually
    # long_description=open('README.txt').read(),
    entry_points={"console_scripts": ["start=ytmusiclibtracker.__main__:main"]},
)
