import requests, json
import warnings

warnings.filterwarnings("ignore")

GOOD_WEATHER_IDS = ['800']
MODERATE_WEATHER_IDS = ['300', '301', '302', '310', '500', '600', '600',
                        '701', '801', '802', '803', '804', '951', '952', 
                        '953', '954', '955', '956', '957', '958']


def weather(lat,lon):
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?lat=' + 
                     str(lat) + '&lon=' + str(lon) + 
                     '&appid=c4c9e375fb418e60e4cd11abac48615d')
    print r.json()
    wid = str(r.json()['weather'][0]["id"])
    print '[WEATHER]', r.json()['weather'][0]['main']
    if wid in GOOD_WEATHER_IDS:
        return 1
    elif wid in MODERATE_WEATHER_IDS:
        return 0
    else:
	    return -1


if __name__ == '__main__':
    print weather(50,50)