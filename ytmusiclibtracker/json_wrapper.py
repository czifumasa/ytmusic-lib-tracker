import json

from ytmusiclibtracker.common import *


def create_json_with_raw_data(output_dir, filename, raw_data, with_timestamp):
    full_name = os.path.join(output_dir,
                             filename + '_' + current_date_time_to_file_name_string() + '.json') if with_timestamp else os.path.join(
        output_dir, filename + '.json')

    with open(full_name, 'w', encoding='utf-8') as json_file:
        json.dump(raw_data, json_file, ensure_ascii=False, indent=2)

    return os.path.abspath(full_name)
