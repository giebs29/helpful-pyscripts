import arcpy
import timeit
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


test_table = r'C:\Users\samg\Documents\MyRepos\blandindatatools\SmartForNew.gdb\BLA_LAYERS\Timber_Sales'

iterations = 100

def table2dict(input_table,fields=False,where=False):
    data = []

    if not fields:
        fields = '*'

    if not where:
        where = ''

    with arcpy.da.SearchCursor(input_table,fields,where) as sc:
        fields = [str(i) for i in sc.fields]
        for row in sc:
            temp_dict = {}
            for col, field in enumerate(fields):
                temp_dict[field] = row[col]
            data.append(temp_dict)
    return data

##sam = table2dict(test_table,['topography'])

data_list1 = table2dict(test_table)

fields = ['topography']

data_list2 = table2dict(test_table,fields)

times_list1 = []

time_list2 = []


for attempt in range(iterations):
    temp_list = []
    start_time = timeit.default_timer()
    for i in range(attempt):

        for  row in data_list1:
             temp_list.append(row['topography'])
    elapsed = timeit.default_timer() - start_time
    times_list1.append(elapsed)

for attempt in range(iterations):
    temp_list = []
    start_time = timeit.default_timer()
    for i in range(attempt):

        for  row in data_list2:
             temp_list.append(row['topography'])
    elapsed = timeit.default_timer() - start_time
    time_list2.append(elapsed)

##for attempt in range(iterations):
##    temp_list = []
##    start_time = timeit.default_timer()
##    for i in range(attempt):
##
##        with arcpy.da.SearchCursor(test_table, '*') as sc:
####        with arcpy.da.SearchCursor(test_table, ['topography']) as sc:
##             for each in sc:
####                 print each[34]
##                 temp_list.append(each[34])
####                 print each[0]
##    elapsed = timeit.default_timer() - start_time
##    cursor_times.append(elapsed)
##
##del temp_list

list1_avg =[sum(times_list1)/iterations]*iterations
list2_avg = [sum(time_list2)/iterations]*iterations

plt.plot(range(1,len(times_list1)+1),times_list1, 'r-', range(1,len(times_list1)+1),list1_avg, 'r--', range(1,len(time_list2)+1),time_list2,'b-',range(1,len(time_list2)+1),list2_avg,'b--')
plt.ylabel('Seconds')
plt.xlabel('Iterations')
plt.show()


