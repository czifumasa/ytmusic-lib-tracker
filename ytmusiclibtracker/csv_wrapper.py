import csv
import io

from ytmusiclibtracker.common import *


def create_csv_with_list_of_dict(output_dir, filename, headers, list_of_rows, with_timestamp):
    full_name = os.path.join(output_dir, filename + '_' + current_date_time_to_file_name_string() + '.csv') if with_timestamp else os.path.join(output_dir, filename + '.csv')

    with io.open(full_name, 'w', encoding="utf-8") as csv_file:
        file_writer = csv.writer(csv_file, delimiter='|', quotechar='`', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        file_writer.writerow(headers)
        for row in list_of_rows:
            file_writer.writerow(row)


def get_list_of_rows_from_file(filename):
    list_of_rows = []
    with io.open(filename, 'r', encoding="utf-8") as csv_file:
        file_reader = csv.reader(csv_file, delimiter='|', quotechar='`', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')

        for row in file_reader:
            list_of_rows.append(row)
    return list_of_rows
