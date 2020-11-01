import sys
from cx_Freeze import setup, Executable

setup(
    name='ytmusiclibtracker',
    url='https://github.com/czifumasa/ytmusic-lib-tracker',
    author='Łukasz Lenart',
    author_email='lukasz.lenart912@gmail.com',
    packages=['ytmusiclibtracker'],
    install_requires=['ytmusicapi >=0.10.1', 'unidecode'],
    version='0.1',
    license='MIT',
    description='Useful tools for youtube music. Exporting library to csv, tracking changes in library, summary of transfer from GPM',
    # We will also need a readme eventually
    long_description=open('README.md').read(),
    entry_points={'console_scripts': ['ytmlt-export=ytmusiclibtracker.__main__:export',
                                      'ytmlt-changelog=ytmusiclibtracker.__main__:changelog']},
    executables=[Executable('ytmusiclibtracker.py', base='console', icon='ytmlt.ico')]
)
