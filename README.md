# ytmusic-lib-tracker 

This project contains useful tools for YouTube Music users:

  * Exporting user's library to csv
  * Listing duplicates on playlist  
  * Tracking changes in user's library
  * Exporting summary of transfer from GPM (WIP)

### Installation

1. [Download Zip file with app.](https://github.com/czifumasa/ytmusic-lib-tracker/releases/latest/download/ytmlt.zip)
1. Extract zip file.

#### Authentication

Before starting, you will also have to provide header file to authenticate api requests to your YouTubeMusic account.
Unfortunately, at least for now, it's a bit complicated.

##### Firefox

1. Open desktop browser and go to [music.youtube.com](https://music.youtube.com)
1. Login to your youtube account
1. Open developer tools by pressing 'F12' or 'Ctrl-Shift-I'  and select the 'Network' tab
1. Click on Home panel in youtube music
1. In developer tools you should see new requests. Type '/browse' to filter.
1. Check if filtered request looks like this: Status 200, Method POST, Domain music.youtube.com
1. Copy the request headers (right click on filtered request > copy > copy request headers)
1. Run ytmusiclibtracker.exe
1. If it's your first time running app, you should this screen:
![IMAGE](https://raw.githubusercontent.com/czifumasa/ytmusic-lib-tracker/cx_freeze/docs/assets/images/welcome_message.JPG) 
1. Paste copied headers into terminal and press `enter` twice
1. That's all! Export of your library should start.

<details>
<summary>You can also watch this gif to make sure you are copying request headers correctly</summary>

![GIF](https://raw.githubusercontent.com/czifumasa/ytmusic-lib-tracker/cx_freeze/docs/assets/images/how_to_copy_headers_firefox.gif)
</details> 

The cookie should not expire, unless you will manually log out of web client.
## Features                                                                                                         
 
### Export 
After correct authentication, export of your library will start automatically. 
Depending on the size of your library it may take some time to finish.
When it's done you should see the proper message:
![IMAGE](https://raw.githubusercontent.com/czifumasa/ytmusic-lib-tracker/cx_freeze/docs/assets/images/welcome_message.JPG) 

Press `Enter` to close application. Then go to the main application folder.
There should be `target` folder where you can find csv files with export results.

### Changelog 
Sometimes some songs in your library or in your playlists may no longer be available on youtube. 
This feature will help in localizing these songs. You can also see what you added and removed since the last export. 

## Advanced Usage
With default behaviour, the last two export files from `target/export` directory will be used as previous and current.
If you want to compare specific files. open `config.ini` file.
In `[Changelog]` section change `auto_detect` option to `0` and modify previous and current file paths.

### Summary of transfer from GPM
Warn: For some users this feature can be unavailable as Google Play Music is shutting down and in some countries it's no longer accessible.

If you want to compare export results from Google Play Music and see what happened after transferring your library to YTM,
you can create csv file with exported playlists using [gmusis-playlist.js](https://github.com/soulfx/gmusic-playlist.js).
Next, move that file to directory with export results (by default it's `/target/export`). 
Then open `config.ini`. In `[Changelog]` section change `auto_detect` option to `0` and set `previous_file` as path to your export file from GPM
and `current_file` as path to your export file from YTM.
  
Finally, you can run ytmusiclibtracker.exe. Now created changelog will compare your GPM and YTM libraries.

## Contribution

If you'd like to contribute to the project or just run scripts directly from python see 
[Documentation for Developers](https://github.com/czifumasa/ytmusic-lib-tracker/blob/cx_freeze/docs/README.md).

## Acknowledgements

The project is using [ytmusicapi](https://github.com/sigma67/ytmusicapi) created by [@sigma67](https://github.com/sigma67)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details


