import urllib2
import json

def test_rest(baseURL):
    values = {
        'f' : 'json'}
    if baseURL.split("/")[-1:] != 'MapServer':
        values['where'] = '1=1'
        values['returnCountOnly'] = 'true'

    request = build_request(baseURL,values)
    response = urllib2.urlopen(request)
    data = json.load(response)

    if len(set(data.keys())&set(['count','layers'])) > 0:
        return True

def build_request(base_url,query_param_dict):
    if 'where' in query_param_dict.keys():
        query_str = '/query?'
    else:
        query_str = '/?'
    for param in query_param_dict.keys():
        query_str += '&{}={}'.format(param,query_param_dict[param])
    return base_url + query_str

if __name__ == '__main__':
    print(test_rest('https://watersgeo.epa.gov/arcgis/rest/services/OWRAD_NP21/STORET_NP21/MapServer/0'))
    print(test_rest('https://map22.epa.gov/arcgis/rest/services/cimc/Cleanups/MapServer'))
