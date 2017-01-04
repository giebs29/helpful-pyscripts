import os, urllib, urllib2, datetime, json
from itertools import tee, izip
import time

class data_log():
    def __init__(self,out_path):
        self.out_path = out_path

    def record(self,data):
        with open(self.out_path, 'a+') as outfile:
            outfile.write(data+'\n')

    def start(self):
        self.record('Start Backup '+ time.strftime("%c"))

    def end(self):
        self.record('End Backup '+ time.strftime("%c"))
        self.add_blank_line()

    def add_blank_line(self):
        self.record('')

### Generate Token ###
def generate_token():
    gtUrl = 'https://www.arcgis.com/sharing/rest/generateToken'
    gtValues = {'username' : 'samg_npgs2',
    'password' : 'june82013',
    'referer' : 'http://www.arcgis.com',
    'f' : 'json' }
    gtData = urllib.urlencode(gtValues)
    gtRequest = urllib2.Request(gtUrl, gtData)
    gtResponse = urllib2.urlopen(gtRequest)
    gtJson = json.load(gtResponse)
    token = gtJson['token']
    return token


def getFields(baseURL):
    token  = generate_token()
    values = {
        'f' : 'json',
        'token' : token,
        'where' : '1=1',
        'outFields' : '*'}

    request = build_request(baseURL,values)
    response = urllib2.urlopen(request)
    data = json.load(response)

    fieldList = [str(i) for i in data['features'][0]['attributes'].keys()]
    return fieldList

def get_oid_field(baseURL):
    token  = generate_token()
    values = {
        'f' : 'json',
        'token' : token}

    request = build_request(baseURL,values)
    response = urllib2.urlopen(request)
    data = json.load(response)
    oid_field = data['objectIdField']
    return oid_field

def build_request(base_url,query_param_dict,query=False):
    if query:
        query_str = '/query?'
    else:
        query_str = '/?'
    for param in query_param_dict.keys():
        query_str += '&{}={}'.format(param,query_param_dict[param])
    return base_url + query_str

def get_json(url,values):
    if 'where' in [i for i in values.keys()]:
        request = build_request(url,values,True)
    else:
        request = build_request(url,values)
    response = urllib2.urlopen(request)
    data = json.load(response)

    return data

def get_max_id(baseURL):
    oid_field = get_oid_field(baseURL)
    token = generate_token()
    where = "1=1"
    max_id = 0
    cont = True
    while cont:
        values = {
            'f' : 'json',
            'where' : where,
            'token' : token,
            'outFields' : oid_field}
        data = get_json(baseURL, values)
        try:
            temp_max_id = max([i['attributes'][oid_field] for i in data['features']])
            if temp_max_id > max_id:
                max_id = temp_max_id
                where ='{}>{}'.format(oid_field,max_id)
        except:
            return max_id

def compile_json(baseURL):
    oid_field = get_oid_field(baseURL)
    token = generate_token()
    max_id = get_max_id(baseURL)
    cont = True
    if max_id > 1000:
        print "Table contains more than 1000 rows"
        break_values = range(0,max_id,1000)
        break_values.append(max_id)

        out_json = None

        for pair in pairwise(break_values):
            oid_min = pair[0]
            oid_max = pair[1]

            print "Retrieving features {}-{}".format(oid_min,oid_max)

            where = '"{}">{}AND"{}"<={}'.format(oid_field,oid_min,oid_field,oid_max)
            values = {
                'f' : 'json',
                'where' : where,
                'token' : token,
                'outFields' : '*',
                'returnGeometry':'true'}

            if not out_json:
                out_json = get_json(baseURL, values)

            else:
                out_json['features'] += get_json(baseURL, values)['features']

        return out_json , max_id
    else:
        print "Table contains less than 1000 rows"
        print "Retrieving features 0-{}".format(oid_max)
        values = {
            'f' : 'json',
            'where' : '1=1',
            'token' : token,
            'outFields' : '*',
            'returnGeometry':'true'}
        return get_json(baseURL, values) , max_id

def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return [i for i in izip(a, b)]

def save_json(data,out_path):
    with open(out_path, 'w') as outfile:
        json.dump(data, outfile)

def featureservice_to_json(rest_url,out_dir):
    token = generate_token()
    values = {
        'f' : 'json',
        'token' : token}
    data = get_json(rest_url, values)

    for layer in data['layers']:
        print('Downloading {} and saving as json'.format(layer['name']))
        url = rest_url + '/' + str(layer['id'])
        json_data , feat_count = compile_json(url)
        bkup_log.record('    {0} contains {1} features'.format(layer['name'],feat_count))
        json_data.update({
            'name' : layer['name'],
            'type' : 'layer'})
        json_path = os.path.join(out_dir,layer['name']+'.json')
        save_json(json_data,json_path)

    for table in data['tables']:
        print('Downloading {} and saving as json'.format(table['name']))
        url = rest_url + '/' + str(table['id'])
        json_data , feat_count = compile_json(url)
        bkup_log.record('    {0} contains {1} rows'.format(table['name'],feat_count))
        json_data.update({
            'name' : table['name'],
            'type' : 'table'})
        json_path = os.path.join(out_dir,table['name']+'.json')
        save_json(json_data,json_path)

def get_feature_service_info(rest_url):
        token = generate_token()
        values = {
            'f' : 'json',
            'token' : token}
        return get_json(rest_url, values)

def log_info(out_path,data):
  with open(out_path, 'a+') as outfile:
      outfile.write(data+'\n')

def create_out_dir(base_path):
    newpath = '{0}\SmartForBackup{1}'.format(base_path,time.strftime("%m%d%y"))
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    return newpath

if __name__ == '__main__':

    bkup_log = data_log(r"C:\Users\samg\Desktop\BLANDIN_JSON\download_log.txt")
    bkup_log.start()

    url = 'http://services1.arcgis.com/wqUJgYYL9SHyZZcr/ArcGIS/rest/services/SmartForWeb_NPGSAGO/FeatureServer'
    json_folder = create_out_dir(r"C:\Users\samg\Desktop\BLANDIN_JSON")

    featureservice_to_json(
        rest_url=url,
        out_dir=json_folder)

    bkup_log.end()
