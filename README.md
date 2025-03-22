# YTMusic-Lib-Tracker

This project contains useful tools for YouTube Music users:

* Exporting user's library to csv or json
* Listing duplicated songs
* Listing unavailable songs
* Tracking changes in user's library
* Exporting summary of transfer from GPM

### Installation

1. [Download Zip file with app.](https://github.com/czifumasa/ytmusic-lib-tracker/releases/latest/download/YTMLibTracker-Windows.zip)
1. Extract zip file.

#### Authentication and Usage

Before starting, you will also have to provide header file to authenticate api requests to your YouTubeMusic account.
Unfortunately, at least for now, it's a bit complicated, so please follow this guide:

1. Open your desktop browser

<details>
 <summary>Instructions for Firefox [CLICK]</summary>

2. Go to [music.youtube.com](https://music.youtube.com)
3. Login to your youtube account
4. Open developer tools by pressing 'F12' or 'Ctrl-Shift-I' and select the 'Network' tab
5. Click on Home panel in youtube music
6. In developer tools you should see new requests. Type '/browse' to filter.
7. Check if filtered request looks like this: Status 200, Method POST, Domain music.youtube.com
8. Copy the request headers (right click on filtered request > copy > copy request headers)
    <details>
    <summary>You can also watch this gif to make sure you are copying request headers correctly [CLICK]</summary>

   ![GIF](https://raw.githubusercontent.com/czifumasa/ytmusic-lib-tracker/master/docs/assets/images/how_to_copy_headers_firefox.gif)
    </details> 

</details>
<details>
 <summary>Instructions for Google Chrome [CLICK]</summary>

2. Go to [music.youtube.com](https://music.youtube.com)
3. Login to your youtube account
4. Open developer tools by pressing 'F12' or 'Ctrl-Shift-I' and select the 'Network' tab
5. Click on Home panel in youtube music
6. In developer tools you should see new requests. Type '/browse' to filter.
7. Check if filtered request looks like this: Status 200, Method POST, Domain music.youtube.com
8. Click on the Name of any matching request. In the `Headers` tab, scroll to the section `Request headers` and copy
   everything starting from `accept: */*` to the end of the section
     <details>
     <summary>You can also watch this gif to make sure you are copying request headers correctly [CLICK]</summary>

   ![GIF](https://raw.githubusercontent.com/czifumasa/ytmusic-lib-tracker/master/docs/assets/images/how_to_copy_headers_chrome.gif)
     </details> 

</details>

9. Once you have copied request headers, run `YTMusicLibTracker.exe`
10. If it's your first time running app, you should this screen:
    ![IMAGE](https://raw.githubusercontent.com/czifumasa/ytmusic-lib-tracker/master/docs/assets/images/welcome_message.JPG)
11. Paste copied headers into terminal and press `enter` twice
12. That's all! Export of your library should start.
13. Depending on the size of your library it may take up to a few minutes to complete the export.
14. When it's done you should see the proper message:
    ![IMAGE](https://raw.githubusercontent.com/czifumasa/ytmusic-lib-tracker/master/docs/assets/images/end_message.JPG)
15. Press `Enter` to close application.
16. Go to the main application folder. Your whole library, uploaded songs and playlist has been exported and saved in
    CSV file.
    With default settings you can find export results in `output\export` directory and changelog in `output\changelog`.

The cookie you used for authentication should not expire, so the next time you run the app, you will be already logged
in.  
However, If you have any problems with authentication, remove `headers_auth.json` file from main application folder and
try to run `YTMusicLibTracker.exe` again to update your cookie file.

## Features

### Export

After correct authentication, export of your library will start automatically.
Depending on the size of your library it may take some time to finish.
With default settings you can find the results saved in `output\export` as csv file. CSV file is using `|` as column
separator. It contains following columns:
`Artists,Title,Album,VideoId,SetVideoId,Playlist,PlaylistId,IsAvailable`

### Export to json

With default settings, your YouTube music library will be exported as csv file containing the most important
information. However, it's possible to export data as raw json file containing everything that's available in
ytmusicapi.

To change export output file:

1. Open `config.ini` file.
2. In `[EXPORT]` section change `output_type` option to `JSON` or `CSV`
3. Save `config.ini` file.

### Changelog

After successfull export, CSV file with changelog data will be created.
With default settings you can find it in `output\changelog` directory.

Changelog will contain:

* Unavailable songs (On the playlists you can see them as greyed out)
* Duplicated songs from your playlists or library
* Songs that you added since last export
* Songs that you removed since last export
* Songs where metadata has been changed by youtube
* All other songs that has not been changed

<details>
     <summary>Example with changelog [CLICK]</summary>

![IMAGE](https://raw.githubusercontent.com/czifumasa/ytmusic-lib-tracker/master/docs/assets/images/csv_examples.jpg)
</details> 

## Advanced Usage

### Switch youtube account

If you want to change the account from you are importing data:

1. Go to application's main folder.
2. Remove `headers_auth.json` file if it exists.
3. Run `YTMusicLibTracker.exe`
4. You will be asked to paste request headers again, so repeat the procedure described
   in [Authentication](#authentication) section.
   This time you should be logged in to your second youtube account.

### Summary of transfer from GPM

Warning: For some users this feature can be unavailable as Google Play Music is shutting down and in some countries it's
no longer accessible.
So it won't be possible to export your GPM library. You can try to workaround it by opening GPM with deeper link instead
of Home Page.
For example this one: [Go to GPM](https://play.google.com/music/listen?u=1#/artists)

If you want to compare export results from Google Play Music and see what happened after transferring your library to
YTM:

1. Run `YTMusicLibTracker.exe` and create export file.
1. Create csv file with exported google play music playlists
   using [gmusis-playlist.js](https://github.com/soulfx/gmusic-playlist.js).
   (Check its documentation for details). Use Google Chrome as it may no longer work in firefox.
2. Move that file to directory with export results (by default it's `/output/export`).
3. Open `config.ini` from app's main folder.
4. In `[Export]` section:
    * change `skip_export` option to `1`
5. In `[Changelog]` section:
    * change `auto_detect` option to `0`
    * set `current_file` option as path to your export file from YTM (The one from first step)
    * set `previous_file` option as path to your export file from GPM (The one from second step)
6. Finally, you can run `YTMusicLibTracker.exe` again. Now created changelog will compare your GPM and YTM libraries.
7. Revert your `config.ini` file to default options, by replacing its content with
   this: [Config.ini](https://raw.githubusercontent.com/czifumasa/ytmusic-lib-tracker/master/config.ini)

### Manual Changelog

With default behaviour, your youtube music library will be exported and changelog will be created based on comparison of
current and previous exports.

If you want to compare specific files:

1. Open `config.ini` file.
2. In `[EXPORT]` section change `skip_export` option to `1`
3. In `[CHANGELOG]` section change `auto_detect` option to `0`
4. In `[CHANGELOG]` section modify `previous_file` and `current_file` with the paths to file you want to use in
   comparison
5. Save `config.ini` file.

## Contribution

If you'd like to contribute to the project or just run scripts directly from python see
[Documentation for Developers](https://github.com/czifumasa/ytmusic-lib-tracker/blob/master/docs/README.md).

## Acknowledgements

The project is using [ytmusicapi](https://github.com/sigma67/ytmusicapi) created
by [@sigma67](https://github.com/sigma67)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details


