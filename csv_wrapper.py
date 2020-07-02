import csv


def create_csv_with_list_of_dict(filename, list_of_rows):

    with open(filename, 'w') as csv_file:
        file_writer = csv.writer(csv_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        for row in list_of_rows:
            file_writer.writerow(row)
