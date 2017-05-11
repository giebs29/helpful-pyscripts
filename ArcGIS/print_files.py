import os
from os import path
import csv
import re



def countPages(filename):
    pdfDoc = arcpy.mapping.PDFDocumentOpen(filename)
    return pdfDoc.pageCount

directory = ""
out_csv = ""
file_type = ".pdf"

with open(out_csv, "w") as csvfile:
    writer = csv.writer(csvfile)
    for path, subdirs, files in os.walk(directory):
       for filename in files:
           if file_type in filename:
                  writer.writerow(os.path.join(path, filename))
