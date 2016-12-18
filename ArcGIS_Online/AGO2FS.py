import os, urllib, urllib2, datetime, json
from itertools import tee, izip

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
        print "Greater than 1000 rows"
        break_values = range(0,max_id,1000)
        break_values.append(max_id)

        out_json = None

        for pair in pairwise(break_values):
            oid_min = pair[0]
            oid_max = pair[1]

            print "Retrieving feature {}-{}".format(oid_min,oid_max)

            where = '"{}">{}AND"{}"<={}'.format(oid_field,oid_min,oid_field,oid_max)
            values = {
                'f' : 'json',
                'where' : where,
                'token' : token,
                'outFields' : '*',
                'returnGeometry':'false'}

            if not out_json:
                out_json = get_json(baseURL, values)

            else:
                out_json['features'] += get_json(baseURL, values)['features']

        return out_json
    else:
        print "Less than 1000 rows"
        values = {
            'f' : 'json',
            'where' : '1=1',
            'token' : token,
            'outFields' : '*',
            'returnGeometry':'true'}
        return get_json(baseURL, values)


def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return [i for i in izip(a, b)]

def save_json(data,out_path):
    with open(out_path, 'w') as outfile:
        json.dump(data, outfile)




token = generate_token()
values = {
    'f' : 'json',
    'returnAttachments' : 'false',
    'token' : token,
    'where' : '1=1',
    'outFields' : '*',
    'returnGeometry' : 'true'}
url = 'http://services1.arcgis.com/wqUJgYYL9SHyZZcr/ArcGIS/rest/services/SmartForWeb_NPGSAGO/FeatureServer/4'
# print get_json(url, values)
# print get_oid_field(url)
# print get_max_id(url)
data = compile_json(url)
save_json(data, r"C:\Users\Sam\Desktop\loc_vol.json")