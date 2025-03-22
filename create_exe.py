import os
import shutil

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
        "build_exe": os.path.join('build', 'target', 'YTMusicLibTracker'),
        'packages': ['ytmusicapi', 'unidecode', 'multiprocessing'],
        'excludes': ['tkinter', 'test', 'unittest', 'pydoc_data'],
        'include_files': ['config.ini'],
        'optimize': 2,
    }},
    executables=[
        Executable('ytmusiclibtracker.py', base='console', icon='ytmlt.ico', target_name='YTMusicLibTracker')]
)


def zip_output():
    zip_path = os.path.join('build', 'zip', 'YTMusicLibTracker')

    shutil.make_archive(zip_path.replace(".zip", ""), 'zip', os.path.join('build', 'target'))
    print(f"Created ZIP archive: {zip_path}")


# If this script is run directly, execute the build + zip process
if __name__ == "__main__":
    zip_output()
