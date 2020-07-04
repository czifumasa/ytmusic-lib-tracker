import csv
import io


def create_csv_with_list_of_dict(filename, headers, list_of_rows):

    with io.open(filename, 'w', encoding="utf-8") as csv_file:
        file_writer = csv.writer(csv_file, delimiter='|', quotechar='`', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        file_writer.writerow(headers)
        for row in list_of_rows:
            file_writer.writerow(row)
