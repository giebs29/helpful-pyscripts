import os
from os import path
import csv
import re
import arcpy



def countPages(filename):
    pdfDoc = arcpy.mapping.PDFDocumentOpen(filename)
    return pdfDoc.pageCount


with open("PDF_List.txt", "w") as csvfile:
    writer = csv.writer(csvfile,delimiter='$')
    for path, subdirs, files in os.walk(r'X:\business\projects\Lake_Connections\Redlines\Redline_PDFs'):
       for filename in files:
           if '.pdf' in filename:
              if 'COMBINED' not in filename.upper():
                  f = os.path.join(path, filename)
                  try:
                      pages = countPages(f)
                      print filename,pages
                  except:
                         print filename,'Cannot open'
                         pages = 'NA'

                  writer.writerow([path] + [filename] + [pages])


print('complete')
