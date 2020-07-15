import codecs
import os
import re
import string
import sys
import time
from datetime import datetime
from difflib import SequenceMatcher

import unidecode

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


def group_list_by_function(seq, function):
    grouped_elements = {}
    for element in seq:
        key = function(element)
        if key in grouped_elements:
            grouped_elements[key].append(element)
        else:
            grouped_elements[key] = [element]
    return grouped_elements


def current_date_time_to_file_name_string():
    return datetime.today().strftime('%Y_%m_%d_%H_%M_%S')


def get_comparable_text(text):
    # omit text in brackets
    t = re.sub(r'[\(\[].*?[\)\]]', '', text)
    # omit punctuation
    t = t.translate(str.maketrans('', '', string.punctuation))
    # trim
    t = t.strip()
    # to lower case
    t = t.lower()
    # normalize by removing diacritics
    t = unidecode.unidecode(t)
    return t


def are_two_texts_similar(t1, t2, expected_ratio):
    similarity = SequenceMatcher(None, t1, t2).quick_ratio()
    if expected_ratio < similarity < 1:
        log(t1 + '  ' + t2)
    return similarity > expected_ratio
