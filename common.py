from gmusicapi import Mobileclient
from gmusicapi.exceptions import CallFailure
from preferences import *
import sys
import os
import codecs
import time
import getpass


# the logfile for keeping track of things
logfile = None

#
# # flag indicating if account is all access capable
# allaccess = True


# opens the log for writing
def open_log(filename):
    global logfile
    logfile = codecs.open(filename, mode='w', encoding='utf-8', buffering=1)
    return logfile


# closes the log
def close_log():
    if logfile:
        logfile.close()


def log(message, nl=True):
    if nl:
        message += os.linesep
    sys.stdout.write(message)
    if logfile:
        logfile.write(message)


def open_api():
    global api
    log('Logging into google music...')
    # get the password each time so that it isn't stored in plain text
    password = getpass.getpass(username + '\'s password: ')

    log('aaa')
    api = Mobileclient()
    if not api.login(username, password, Mobileclient.FROM_MAC_ADDRESS):
        log('ERROR unable to login')
        time.sleep(3)
        exit()

    log('Login Successful.')
    log('Available track details: ' + str(get_google_track_details()))
    return api


# logs out of the google music api
def close_api():
    if api:
        api.logout()


def list_duplicates(seq):
    seen = set()
    seen_add = seen.add
    # adds all elements it doesn't know yet to seen and all other to seen_twice
    seen_twice = set(x for x in seq if x in seen or seen_add(x))
    # turn the set into a list (as requested)
    return list(seen_twice)


# gets the track details available for google tracks
def get_google_track_details(sample_song='one u2'):
    results = aa_search(sample_song, 1)
    if len(results):
        return results[0].get('track').keys()
    return "['title','artist','album']"


# search all access
def aa_search(search_string, max_results):
    global allaccess
    results = []
    if allaccess:
        try:
            results = api.search(search_string,
                                 max_results=max_results).get('song_hits')
        except CallFailure:
            allaccess = False
            log('WARNING no all access subscription detected. ' +
                ' all access search disabled.')
    return results


# loads the personal library
def load_personal_library():
    log('Loading personal library... ')
    plib = api.get_all_songs()
    log('done. '+str(len(plib))+' personal tracks loaded.')
    return plib
