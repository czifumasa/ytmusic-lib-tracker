from ytmusicapi import YTMusic
from common import *
import json


def open_api():
    log('Logging into YouTube Music...')
    api = YTMusic('headers_auth.json')
    log('Login Successful.')
    return api


def get_my_playlist_ids(api):

    my_playlists = api.get_library_playlists()
    playlist_ids = []
    for playlist in my_playlists:
        # TODO create constants
        playlist_ids.append(playlist['playlistId'])
    return playlist_ids


def get_songs_from_playlist_by_id(songs_list):
    songs_by_id = {}

    for track in songs_list:
        songs_by_id[track['videoId']] = track

    return songs_by_id


def list_duplicated_songs_in_playlist(api, playlist_id):

    playlist = api.get_playlist(playlist_id, 5000)
    songs = playlist['tracks']

    log('Duplicated items in playlist: ' + playlist['title'])

    video_ids = []
    for song in songs:
        video_ids.append(song['videoId'])

    duplicated_ids = list_duplicates(video_ids)

    songs_by_ids = get_songs_from_playlist_by_id(songs)

    duplicated_song_strings = []
    for dupe in duplicated_ids:
        duplicated_song_strings.append(song_string_representation(songs_by_ids[dupe]))

    return duplicated_song_strings


def song_string_representation(song):

    artists = song['artists']
    title = song['title']

    return artists[0]['name'] + ' - ' + title


def setup_ytm_login():
    YTMusic.setup(filepath='headers_auth.json', headers_raw='POST /youtubei/v1/browse?alt=json&key'
                                                            '=AIzaSyC9XL3ZjWddXya6X74dJoCTL-WEYFDNX30 HTTP/1.1\r\nHost: '
                                                            'music.youtube.com\r\nUser-Agent: Mozilla/5.0 (Windows NT '
                                                            '10.0; Win64; x64; rv:77.0) Gecko/20100101 '
                                                            'Firefox/77.0\r\nAccept: */*\r\nAccept-Language: pl,'
                                                            'en-US;q=0.7,en;q=0.3\r\nAccept-Encoding: gzip, deflate, '
                                                            'br\r\nContent-Type: application/json\r\nContent-Length: '
                                                            '1218\r\nX-Goog-Visitor-Id: '
                                                            'Cgt6TXNadUlJUkFaOCjAleP3BQ%3D%3D\r\nX-Goog-AuthUser: '
                                                            '0\r\nx-origin: '
                                                            'https://music.youtube.com\r\nX-YouTube-Client-Name: '
                                                            '67\r\nX-YouTube-Client-Version: 0.1\r\nX-YouTube-Device: '
                                                            'cbr=Firefox&cbrver=77.0&ceng=Gecko&cengver=77.0&cos=Windows'
                                                            '&cosver=10.0\r\nX-Youtube-Identity-Token: '
                                                            'QUFFLUhqa29kbW9SNnA2WnNqVG04RW5KcVBPYTJMU0pBQXw=\r\nX'
                                                            '-YouTube-Page-CL: 317646540\r\nX-YouTube-Page-Label: '
                                                            'youtube.music.web.client_20200622_00_RC00\r\nX-YouTube-Utc'
                                                            '-Offset: 120\r\nX-YouTube-Time-Zone: '
                                                            'Europe/Warsaw\r\nX-YouTube-Ad-Signals: '
                                                            'dt=1593363136897&flash=0&frm&u_tz=120&u_his=1&u_java&u_h'
                                                            '=1080&u_w=1920&u_ah=1040&u_aw=1920&u_cd=24&u_nplug=1&u_nmime'
                                                            '=2&bc=29&bih=507&biw=1920&brdim=1912%2C-8%2C1912%2C-8%2C1920'
                                                            '%2C0%2C1936%2C1056%2C1920%2C507&vis=1&wgl=true&ca_type=image'
                                                            '\r\nOrigin: https://music.youtube.com\r\nAuthorization: '
                                                            'SAPISIDHASH '
                                                            '1593363137_9f81e24fcf20c48590c4cfb315b0b337cce934eb\r'
                                                            '\nReferer: https://music.youtube.com/\r\nConnection: '
                                                            'keep-alive\r\nCookie: CONSENT=YES+PL.pl+20150705-15-0; '
                                                            'VISITOR_INFO1_LIVE=zMsZuIIRAZ8; '
                                                            'PREF=volume=100&al=en%2Bpl&activity_based_recommendations=MUSIC_ACTIVITY_MASTER_SWITCH_ENABLED&f6=400&library_tab_browse_id=FEmusic_liked_playlists&f5=30; __Secure-3PSID=ygdAliniDHu6hrvXDplXDPKq4mDf89KrFWv1ZVm5GVJftz3XUg-2_cHsS0cBiKcD9fpWWA.; __Secure-HSID=AFfroTN0_tEPEwuSF; __Secure-SSID=Al_yYWT_iEaTapO-o; __Secure-APISID=w3Q2pUp_wbTLooS6/AemWxCgln99rMQII3; __Secure-3PAPISID=8SGxFUIZyFsk3dAp/A4tdQxJTM5Z7_YH9U; SID=ygdAliniDHu6hrvXDplXDPKq4mDf89KrFWv1ZVm5GVJftz3X9S0E9_qpvZqh0qgv0NWoYw.; HSID=AFfroTN0_tEPEwuSF; SSID=Al_yYWT_iEaTapO-o; APISID=w3Q2pUp_wbTLooS6/AemWxCgln99rMQII3; SAPISID=8SGxFUIZyFsk3dAp/A4tdQxJTM5Z7_YH9U; LOGIN_INFO=AFmmF2swRQIhAMkpnqoy_2aYuKOWWxRq-lFgbo5InZ1OFE31SAblRBSoAiA26IOYQIz2El18fJ4-oK8ZHcojZ4WX-xZOCvelFVc5Jg:QUQ3MjNmdzIyTUdrQTlmTnBqVWtfRzhoTmlNbDlkX2xEVnBtZkxfeHpUaEV0TUp6ZW8xNTBDSmZDTkU5MnU0YlZQUmFDMkFSbWNIUkZjR1BGRm13aEhqX0NuaFJHNllzaXdqdVduSjlEb3dSR3dmbFpZRGtoZkVOX3p5V0RrRkJvUkc5b3ZMaFRvcEgyMloyczVHVFZGREZ5RlQtV3k4ZzdjR3lGNWFSektUQ2J6YzNHdHJOYlYxaWNaWkJEX2w1MXdMQmlZR3BTM1REM2pKOWV5MFpyRHFpV2dfWlZfdU5zcW9RbUc2eXd0QTRzYnNzMUQxLTFjcFp5MGQ0R3owU2l1dlVYb3JsMWFaNA==; SIDCC=AJi4QfHNIHH6-GZ7m5LSG6G5oBGd-rrghMdSMFkaGPJUHLKUJHbeYS3UpLPhkvgkCSNcQeElWQ; YSC=hEJF-VdzkPQ\r\nCache-Control: max-age=0')
