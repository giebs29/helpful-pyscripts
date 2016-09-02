import arcpy
import json
import requests

def getFields(baseURL):
    where = "1=1"
    fields = "*"

    query = "?where={}&outFields={}&returnGeometry=true&f=json".format(where, fields)

    fsURL = baseURL + query

    req = requests.get(fsURL)

    a = json.loads(req.text)

    fieldList = [str(i) for i in a['features'][0]['attributes'].keys()]
    return fieldList

def getMaxID(baseURL):
    count = '1=1'
    cont = True

    while count > True:
        where = "{}".format(count)
        fields = "OBJECTID"

        query = "?where={}&outFields={}&returnGeometry=true&f=json".format(where, fields)

        fsURL = baseURL + query

        req = requests.get(fsURL)

        a = json.loads(req.text)

        try:
            b = max([i['attributes']['OBJECTID'] for i in  a['features']])
            count = 'OBJECTID > {}'.format(b)
            print b
        except:
            print "Largest object ID: ",count.split()[2]
            cont = False
            return count.split()[2]

def createQueryList(maxID):
    maxID = int(maxID)
    queryList = []
    low = 1
    high = 1000

    for num in range(0,(maxID/1000)+1):

        if high < maxID:
            where = "OBJECTID BETWEEN {0} AND {1}".format(low, high)
            queryList.append(where)

            low += 1000
            high += 1000

        else:
            where = "OBJECTID BETWEEN {0} AND {1}".format(low, maxID)
            queryList.append(where)
            return queryList

def export2FS(queryList, baseURL, useFields, outPath):
    arcpy.env.workspace = 'in_memory'

    if useFields == True:
        fields = '*'
        # fields = getFields(baseURL)
        # fields  = str(fields).replace('[','')
        # fields  = str(fields).replace(']','')
        # fields  = str(fields).replace("'",'')
        print fields

    else:
        fields =''

    fileList = []

    for num, each in enumerate(queryList):

        arcpy.env.overwriteOutput = True
        where = each

        query = "?where={}&outFields={}&returnGeometry=true&f=json".format(each, fields)

        fsURL = baseURL + query

        fs = arcpy.FeatureSet()

        fs.load(fsURL)
        name = 'temp' + str(num)
        print name

        fileList.append(name)
        arcpy.CopyFeatures_management(fs, name)

    arcpy.Append_management((fileList[1:]),(fileList[0]))
    arcpy.CopyFeatures_management((fileList[0]), outPath)


    for each in fileList:
        arcpy.Delete_management(each)

def restService2FeatureService(baseURL, outPath):
    if '/query' not in baseURL:
        baseURL += '/query'

    maxID =  getMaxID(baseURL)
    qList = createQueryList(maxID)

    export2FS(qList, baseURL, True, outPath)

##    try:
##        export2FS(qList, baseURL, True, outPath)
##    except:
##        export2FS(qList, baseURL, False, outPath)


baseURL = 'http://www.carltoncountygis.com/arcgis/rest/services/AGOL/AGO_Internal_Viewer/MapServer/4'
outfile = r"C:\Users\samg\Desktop\carlton_county.gdb\carlton_parcels_083116"

restService2FeatureService(baseURL,outfile)
