import csv_handler as csvh
import util


if __name__ == "__main__":
    input_csv = "input_paths.csv"
    rows = csvh.read_all_csv(input_csv)
    print(rows)
    found_paths = util.get_fpaths_from_all_paths(map(lambda x: x[-1], rows)) # last element of a row is the path
    
    """
    for p in found_paths:
        print(p)
    #
    """
    
    csvh.write_rows("out.csv", map(lambda x: [x], found_paths))