from cx_Freeze import setup, Executable

setup(
    name='YtMusic-Lib-Tracker',
    url='https://github.com/czifumasa/ytmusic-lib-tracker',
    author='Łukasz Lenart',
    author_email='lukasz.lenart912@gmail.com',
    version='0.1',
    license='MIT',
    description='Useful tools for youtube music. Exporting library to csv or json, tracking changes in library, summary of transfer from GPM',
    long_description=open('README.md').read(),
    options={"build_exe": {
        'packages': ['ytmusicapi', 'unidecode', 'multiprocessing'],
        'excludes': ['tkinter', 'test', 'unittest', 'pydoc_data'],
        'include_files': ['config.ini'],
        'optimize': 2,
    }},
    executables=[Executable('ytmusiclibtracker.py', base='console', icon='ytmlt.ico', target_name='YTMusicLibTracker')]
)
