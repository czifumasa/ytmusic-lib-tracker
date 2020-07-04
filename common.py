import codecs
import os
import sys
import time

# the logfile for keeping track of things
logfile = None


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


def create_dir_if_not_exist(path_to_dir):
    if not os.path.exists(path_to_dir):
        os.makedirs(path_to_dir)


def throw_error(message):
    log(message)
    time.sleep(3)
    exit()


def flatten_list(list_to_flatten):
    return [item for sublist in list_to_flatten for item in sublist]


def get_duplicated_items_from_list(seq):
    seen = set()
    seen_add = seen.add
    # adds all elements it doesn't know yet to seen and all other to seen_twice
    seen_twice = set(x for x in seq if x in seen or seen_add(x))
    # turn the set into a list (as requested)
    return list(seen_twice)
