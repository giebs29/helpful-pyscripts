#http://stackoverflow.com/questions/7991209/identifying-excel-sheet-cell-color-code-using-xlrd-package
import arcpy
import xlrd
import csv
import os



def retrieve_sheet(doc_path):
    # Retrieve sheet name from doc string
    if "$" in doc_path:
       sheet_name = (doc_path.split("\\")[-1:][0]).replace("$","")
       return sheet_name
    else:
         return

def clean_doc_path(doc_path):
    # Removes sheet from doc path
    if "$" in doc_path:
       temp_string = ""
       for each in doc_path.split("\\")[:-1]:
           temp_string = os.path.join(temp_string,each)
       return temp_string
    else:
         return doc_path



def get_cell_data(doc_path,sheet_name,table_type,addr_col_name,city_col_name):

    output_list = []

    book = xlrd.open_workbook(doc_path, formatting_info=True)
    sheet = book.sheet_by_name(sheet_name)
    rows, cols = sheet.nrows, sheet.ncols

    fields = []

    for col in range(cols):
        pre_cell = sheet.cell(0, col)
        fields.append(str(pre_cell.value))

    try:
        addr_col_index = fields.index(arcpy.GetParameterAsText(1))
        city_col_index = fields.index(arcpy.GetParameterAsText(2))
    except:
##           arcpy.AddMessage([int(s) for s in arcpy.GetParameterAsText(1).split() if s.isdigit()])
           addr_col_index = [int(s) for s in arcpy.GetParameterAsText(1).split('Field') if s.isdigit()][0] - 1
           city_col_index = [int(s) for s in arcpy.GetParameterAsText(2).split('Field') if s.isdigit()][0] - 1

    #Skip the header row
    for row in range(rows)[1:]:
        col = 0
        addr_cell = sheet.cell(row, addr_col_index)
        city_cell = sheet.cell(row, city_col_index)

        address = str(addr_cell.value) +" "+ str(city_cell.value)
        try:
            address = address.replace('MN','')
        except:
               pass

        try:
            address = address.replace(',','')
        except:
               pass
        address = address.strip().upper()
        xfx = sheet.cell_xf_index(row, addr_col_index)
        xf = book.xf_list[xfx]
        bgx = xf.background.pattern_colour_index

        # Assign status
        if len(address) > 0:
           if table_type == 'INSTALL':
              # Assign status based on cell color
              # 9 = white
              # 64 = white
              # 10 = red
              # 11 = Green
              # 15 = Turquise
              # 13 = Yellow
              if bgx == 10:
                 status = "INSTALLED"
              elif bgx == 11:
                   status = "READY_FOR_DROP"
              else:
                   status = "FUTURE_DROP"

           elif table_type == 'CANCELLED':
                status = "CANCELLED"

           elif table_type == 'CSR':
                status = "INSTALLED"

           output_list.append((address,status))

    return output_list


def write_csv(data,table_type,out_csv):
    if table_type == 'CSR':
       data = set(data)

    with open(out_csv, 'w',newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['ADDRESS_CITY'] + ['DROP_STATUS'])
        for row in data:
            csv_writer.writerow([row[0]] + [row[1]])




def main():
    arcpy.AddMessage(
    arcpy.GetParameterAsText(0)+
    arcpy.GetParameterAsText(1)+
    arcpy.GetParameterAsText(2)+
    arcpy.GetParameterAsText(3)+
    arcpy.GetParameterAsText(4)+
    arcpy.GetParameterAsText(5)+
    arcpy.GetParameterAsText(6))

    doc = arcpy.GetParameterAsText(0)
    addr_col_name = arcpy.GetParameterAsText(1)
    city_col_name = arcpy.GetParameterAsText(2)
    installs = arcpy.GetParameterAsText(3)
    cancelled = arcpy.GetParameterAsText(4)
    csr = arcpy.GetParameterAsText(5)
    out_csv = arcpy.GetParameterAsText(6)

    # check to make sure the input file is a .xls
    if '.xls' in doc and '.xlsx' not in doc:
       pass
    else:
         arcpy.AddError("Input must be .xls!")
         return

    doc_path = clean_doc_path(doc)

    sheet = retrieve_sheet(doc)



    if [installs,cancelled,csr].count('true') != 1:
       arcpy.AddError("Error")
       return
    else:
         if installs == 'true':
            table_type = 'INSTALL'
         if cancelled == 'true':
            table_type = 'CANCELLED'
         if csr == 'true':
            table_type = 'CSR'

    cell_data = get_cell_data(doc_path,sheet,table_type,addr_col_name,city_col_name)
    write_csv(cell_data,table_type,out_csv)

if __name__ == '__main__':
    main()


