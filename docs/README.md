# ytmusic-lib-tracker (for Devs)

### Regular installation

##### Prerequisites

* [Python](https://www.python.org/downloads/) - version 3.8 or higher

##### Setup

Clone the project into your local machine. To start working with application, open terminal in the project's root folder
and type:

```
 python setup.py install
```

This command will install all required dependencies.

##### Authentication

Before starting, you will also have to provide header file to authenticate api requests to your YouTubeMusic account.
Unfortunately, at least for now, it's a bit complicated.

Follow instruction from [ytmusicapi's documentation](https://ytmusicapi.readthedocs.io/en/latest/setup.html) to
create `headers_auth.json` and copy it to the project's root directory. That file will contain a header with a cookie
and will be used to authenticate all api requests with your YTMusic account.
The cookie should not expire, unless you will manually log out of web client.

### Virtual environment installation (OPTIONAL)

##### Prerequisites

* [pipenv](https://github.com/pypa/pipenv) - install with `pip install pipenv`

##### Setup

Alternatively you can work with application in isolated virtual environment. It's really helpful if you are working with
many python apps and each one of them requires different libraries with conflicting versions.
To create virtual environment you can use pipenv. Open terminal in the project's root folder and type:

 ```
 pipenv install -e .
 ```

Then whenever you'd like to work with application, open shell with activated virtual environment, by typing:

 ```
 pipenv shell
 ```

## Usage

##### Export library and playlists to csv

To export full content of your YTMusic library as well as all your playlists run from project's root folder:

 ```
 ytmlt-export
 ```

##### Tracking changes in user's library

To create changelog run from project's root folder:

 ```
 ytmlt-changelog
 ```

With default behaviour, the last two export files from `ytmlt-export` will be used as previous and current.

##### Export and changelog in single call

Run from project's root folder:

 ```
  python -m ytmusiclibtracker
 ```

##### Create exe

Python scripts can be frozen and delivered as executable. It can be created
using [cx_freeze](https://github.com/marcelotduarte/cx_Freeze).

```
python create_exe.py build
```

In `build/target` directory there will be a folder containing libs and `YTMusicLibTracker.exe` and in `build/zip`
directory there will be compressed zip file ready for release.

##### Run with local ytmusicapi build

In order to test with local ytmusicapi version run:

```
pip uninstall ytmusicapi
pip install ytmusicapi path/to/local/ytmusicapi
```

