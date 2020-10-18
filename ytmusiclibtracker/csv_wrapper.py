import csv
import io

from ytmusiclibtracker.common import *


def create_csv_with_list_of_dict(output_dir, filename, headers, list_of_rows, with_timestamp):
    full_name = os.path.join(output_dir,
                             filename + '_' + current_date_time_to_file_name_string() + '.csv') if with_timestamp else os.path.join(
        output_dir, filename + '.csv')

    with io.open(full_name, 'w', encoding="utf-8") as csv_file:
        file_writer = csv.writer(csv_file, delimiter='|', quotechar='`', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        file_writer.writerow(headers)
        for row in list_of_rows:
            file_writer.writerow(row)


def get_list_of_rows_from_file(filename):
    list_of_rows = []
    with io.open(filename, 'r', encoding="utf-8") as csv_file:
        # detect delimiter
        temp_lines = csv_file.readline() + '\n' + csv_file.readline()
        dialect = csv.Sniffer().sniff(temp_lines, delimiters="|,")
        csv_file.seek(0)

        file_reader = csv.reader(csv_file, dialect)

        for row in file_reader:
            list_of_rows.append(row)
    return list_of_rows


def get_convert_function_by_headers(header):
    if header == get_ytmlt_export_headers():
        return lambda row: row
    if header == get_gpm_export_headers():
        return lambda row: convert_gpm_to_ytmlt_row(row)
    throw_error('CSV file with exported songs has unrecognized structure')


def get_gpm_export_headers():
    return ['title', 'artist', 'album', 'track', 'duration', 'id', 'idtype',
            'playcount', 'rating', 'year', 'genre', 'notes', 'playlist']


def get_ytmlt_export_headers():
    return ['Artists', 'Title', 'Album', 'VideoId', 'SetVideoId', 'Playlist', 'PlaylistId', 'IsAvailable']


def convert_gpm_to_ytmlt_row(gpm_rom):
    expected_order = [1, 0, 2, -1, -1, 12, -1, -1]
    ytmlt_row = [gpm_rom[i] if i >= 0 else '' for i in expected_order]
    return ytmlt_row
