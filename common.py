import sys
import os
import codecs


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


def get_duplicated_items_from_list(seq):
    seen = set()
    seen_add = seen.add
    # adds all elements it doesn't know yet to seen and all other to seen_twice
    seen_twice = set(x for x in seq if x in seen or seen_add(x))
    # turn the set into a list (as requested)
    return list(seen_twice)

