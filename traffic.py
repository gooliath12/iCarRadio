import requests
import json

def traffic(coordinates=['40.7128, -74.0059,1']):
    r = requests.request('get', 'https://traffic.cit.api.here.com/traffic/6.1/flow.json',
                        params={'app_id':['vbmECPJZjFd55Qjd2JhU'],
                        'app_code': ['V17J9DdXQTuSDAWiFyH2vg'],
                        'prox': coordinates}
                        )

    text = json.loads(r.text)

    direction = text['RWS'][0]['RW'][0]['FIS'][0]['FI'][0]['TMC']['QD']
    jamFactor = text['RWS'][0]['RW'][0]['FIS'][0]['FI'][0]['CF'][0]['JF']
    speed = text['RWS'][0]['RW'][0]['FIS'][0]['FI'][0]['CF'][0]['SP']
    freeFlow = text['RWS'][0]['RW'][0]['FIS'][0]['FI'][0]['CF'][0]['FF']
    # text['RWS'][0]['RW'] length is not 1
    #print json.dumps(text, indent=4)
    '''
    print text['RWS'][0]['RW'][1]
    print direction
    print jamFactor
    print speed
    print freeFlow
    # print text
    '''
    return direction, jamFactor, speed, freeFlow