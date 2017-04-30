import requests
import json

def weather(city = 'New York'):

    r = requests.request('get', 'https://weather.cit.api.here.com/weather/1.0/report.json',
                        params={'app_id':['DemoAppId01082013GAL'], 'app_code': ['AJKnXv84fjrb0KIHawS0Tg'],
                        'product': ['observation'], 'name': city}
                    )

    # r.headers['content-type']
    text = json.loads(r.text)
    for i in range(len(text['observations']['location'])):
        # print text['observations']['location'][i]['observation'][0]['city']
        if text['observations']['location'][i]['observation'][0]['city'] == city:
            return text['observations']['location'][i]['observation'][0]['temperature']
    return "cannot find this location"
