import csv


CSV_DELIMITER = ';'
CSV_QUOTECHAR = '"'


def should_accept_element(element, filter_functions):
    for func in filter_functions:
        if func(element) == False:
            return False
        #
    #
    return True
#


def read_all_csv(path, row_filters=None):
    with open(path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=CSV_DELIMITER,
                            quotechar=CSV_QUOTECHAR, quoting=csv.QUOTE_MINIMAL)
        #
        line_list = []
        for row in reader:
            if row_filters == [] or row_filters == None:
                line_list.append(row)
            elif should_accept_element(row, row_filters):
                line_list.append(row)
            else:
                continue
            #
        #
        return line_list
    #
#


def write_rows(csv_name, row_iter):
    with open(csv_name, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=CSV_DELIMITER,
                                quotechar=CSV_QUOTECHAR, quoting=csv.QUOTE_MINIMAL)
        #
        for row in row_iter:
            writer.writerow(row)
    #
#