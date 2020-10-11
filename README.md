# ytmusic-lib-tracker 

This project contains useful tools for YouTube Music users:

  * Exporting user's library to csv
  * Listing duplicates on playlist  
  * Tracking changes in user's library
  * Exporting summary of transfer from GPM (WIP)
  
  
It's still a work in progress. Most of the listed functionalities are working, but they require polishing and they need to be made more user friendly.  

### Regular installation

##### Prerequisites

* [Python](https://www.python.org/downloads/) - version 3.8 or higher

##### Setup

Clone the project into your local machine. To start working with application, open terminal in the project's root folder and type:
```
 python setup.py install
```

This command will install all required dependencies. 

##### Authentication

Before starting, you will also have to provide header file to authenticate api requests to your YouTubeMusic account.
Unfortunately, at least for now, it's a bit complicated.

Follow instruction from [ytmusicapi's documentation](https://ytmusicapi.readthedocs.io/en/latest/setup.html) to create `headers_auth.json` and copy it to the project's root directory. That file will contain a header with a cookie and will be used to authenticate all api requests with your YTMusic account.
The cookie should not expire, unless you will manually log out of web client.
    
### Virtual environment installation (OPTIONAL)

##### Prerequisites

* [pipenv](https://github.com/pypa/pipenv) - install with `pip install pipenv`
                                                       
##### Setup

Alternatively you can work with application in isolated virtual environment. It's really helpful if you are working with many python apps and each one of them requires different libraries with conflicting versions.
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

To export full content of your YTMusic library as well as all your playlists run:

 ```
 ytmlt-export
 ```

##### Listing duplicates 

To export list of duplicated tracks on your playlists run:
 ```
 ytmlt-duplicates
 ```

##### Tracking changes in user's library

When you have at least two export results, you can track any changes in your library.
Sometimes some songs in your library may no longer be available on youtube. This feature will help in localizing unavailable songs. You can also 
see what you added and removed since the last export. Method supports export results 
from `ytmlt-export` and [gmusis-playlist.js](https://github.com/soulfx/gmusic-playlist.js).

 To create changelog run:

 ```
 ytmlt-changelog
 ```
 
With default behaviour, the last two export files from `ytmlt-export` will be used as previous and current.
If you want to compare specific files. open `config.ini` file and provide output directory, previous and current file.

If you want to compare export results from GPM and see what happened after transferring your library to YTM,
you can create csv file with exported playlists using [gmusis-playlist.js](https://github.com/soulfx/gmusic-playlist.js).
Next, move that file to directory with export results (by default it's `/target/export`). 
Then open `config.ini` and replace previous_file option with the path to your CSV file. 
Finally, you can run `ytmlt-changelog`.

## Acknowledgements

The project is using [ytmusicapi](https://github.com/sigma67/ytmusicapi) created by [@sigma67](https://github.com/sigma67)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details


