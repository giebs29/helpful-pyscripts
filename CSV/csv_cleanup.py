import csv
import os
from shutil import copyfile

def remove_bad_rows(in_csv):
    # Build temp csv path
    dir = os.path.dirname(in_csv)
    name = "temp_" + os.path.basename(in_csv)
    temp_csv = os.path.join(dir,name)

    with open(in_csv, 'rb') as in_file:
        with open(temp_csv, 'wb') as out_file:
            writer = csv.writer(out_file)

            # Write all rows that contain data except for first and last
            for row in [i for i in csv.reader(in_file) if i][1:-1]:
                writer.writerow(row)

    # Replace original csv
    copyfile(temp_csv,in_csv)

    # Delete temp csv
    os.remove(temp_csv)
