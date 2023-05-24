import codecs
import configparser
import os
import re
import string
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


def log(message, nl=False):
    if nl:
        message += os.linesep
    print(message)
    if logfile:
        logfile.write(message)


def get_configuration_from_file(filename):
    config = configparser.ConfigParser()
    config.read(filename)
    return config


def get_int_value_from_config(config, section, param_name):
    value = config[section][param_name]
    try:
        return int(value)
    except ValueError:
        throw_error('Error during reading configuration file for option "%s". "%s" cannot be converted to an int' % (
            param_name, value))


def create_dir_if_not_exist(path_to_dir):
    if not os.path.exists(path_to_dir):
        os.makedirs(path_to_dir)


def get_list_of_csv_files_with_timestamp_from_dir(path_to_dir, filename_prefix):
    list_of_files = []
    for (dir_path, dir_names, filenames) in os.walk(path_to_dir):
        # regex for filenames with timestamp matching (filename_prefix_%Y_%m_%d_%H_%M_%S)
        regex_pattern = filename_prefix + '_[0-9]{4}_(0[1-9]|1[012])_(0[1-9]|[12][0-9]|3[01])_([01][0-9]|2[0-3])(_[0-5][0-9]){2}.csv'
        list_of_files.extend([name for name in filenames if re.match(regex_pattern, name)])
    return list_of_files


def throw_error(message):
    raise Exception(message)


def flatten_list(list_to_flatten):
    return [item for sublist in list_to_flatten for item in sublist]


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


def get_comparable_text(text, omit_brackets=False):

    t = text

    if omit_brackets:
        # omit text in brackets
        t = re.sub(r'[\(\[].*?[\)\]]', '', text)
    # replace apostrophe
    t = t.replace('’', '\'')
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
    return similarity > expected_ratio


def get_similarity_index_based_on_length(t1, t2):
    length = len(t1) if len(t1) > len(t2) else len(t2)
    if length < 6:
        return 0.79
    if length > 18:
        return 0.95
    return 0.89
