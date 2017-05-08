import requests
import json
des = {'morning_clouds': '1', 'passing_clouds': '1', 'tstorms_late': '-1', 'scattered_flurries': '-1',
       'night_low_level_haze': '-1', 'night_scattered_clouds': '0', 'light_icy_mix_early': '-1',
       'early_fog_followed_by_sunny_skies': '-1', 'rain_early': '-1', 'night_broken_clouds': '1',
       'night_tstorms': '-1', 'blizzard': '-1', 'passing_showers': '-1', 'sprinkles_early': '-1',
       'tons_of_rain': '-1', 'broken_clouds': '0', 'tropical_storm': '-1', 'night_morning_clouds': '1',
       'heavy_rain_early': '-1', 'night_light_showers': '-1', 'high_clouds': '0', 'night_mostly_cloudy': '1',
       'night_sprinkles': '-1', 'afternoon_clouds': '1', 'sunny': '1', 'more_clouds_than_sun': '0',
       'heavy_snow_early': '-1', 'flurries_late': '-1', 'sleet': '-1', 'light_snow_late': '-1',
       'light_mixture_of_precip': '-1', 'light_snow_showers': '-1', 'night_scattered_tstorms': '-1', 'cloudy': '0',
       'low_level_haze': '-1', 'tstorms': '-1', 'snowstorm': '-1', 'lots_of_rain': '-1', 'light_rain_late': '-1',
       'night_decreasing_cloudiness': '0', 'heavy_rain_late': '-1', 'night_high_clouds': '0',
       'decreasing_cloudiness': '0', 'rain_showers': '-1', 'severe_thunderstorms': '-1', 'sprinkles_late': '-1',
       'night_a_few_showers': '-1', 'widely_scattered_tstorms': '-1', 'light_snow': '-1', 'early_fog': '-1',
       'drizzle': '-1', 'mostly_cloudy': '0', 'night_passing_clouds': '0', 'night_widely_scattered_tstorms':
           '-1', 'dense_fog': '-1', 'night_partly_cloudy': '1', 'night_clearing_skies': '0', 'hurricane': '-1',
       'light_fog': '-1', 'haze': '-1', 'fog': '-1', 'night_passing_showers': '-1', 'light_showers': '-1',
       'breaks_of_sun_late': '1', 'mixture_of_precip': '-1', 'isolated_tstorms_late': '-1', 'night_mostly_clear': '0',
       'hazy_sunshine': '0', 'scattered_tstorms': '-1', 'night_isolated_tstorms': '-1',
       'an_icy_mix_changing_to_rain': '-1', 'night_afternoon_clouds': '1', 'snow_changing_to_rain': '-1',
       'smoke': '-1', 'night_clear': '1', 'mostly_clear': '1', 'duststorm': '-1', 'increasing_cloudiness': '1',
       'ice_fog': '-1', 'snow_flurries': '-1', 'showers_late': '-1', 'night_showers': '-1', 'thundershowers': '-1',
       'flurries_early': '-1', 'tstorms_early': '-1', 'icy_mix_late': '-1', 'more_sun_than_clouds': '1',
       'scattered_clouds': '1', 'night_rain_showers': '-1', 'showery': '-1', 'flash_floods': '-1', 'night_haze': '-1',
       'scattered_tstorms_late': '-1', 'heavy_snow': '-1', 'partly_cloudy': '1', 'snow_showers': '-1',
       'heavy_snow_late': '-1', 'rain_late': '-1', 'night_smoke': '-1', 'icy_mix_early': '-1',
       'cw_no_report_icon': '0', 'a_few_showers': '-1', 'a_mixture_of_sun_and_clouds': '1', 'hail': '-1',
       'snow_early': '-1', 'moderate_snow': '-1', 'showers_early': '-1', 'clearing_skies': '1', 'sandstorm': '-1',
       'passing_clounds': '1', 'an_icy_mix_changing_to_snow': '-1', 'rain_changing_to_snow': '-1',
       'night_a_few_tstorms': '-1', 'night_high_level_clouds': '0', 'freezing_rain': '-1', 'light_freezing_rain': '-1',
       'night_scattered_showers': '-1', 'showers': '-1', 'strong_thunderstorms': '-1', 'light_icy_mix_late': '-1',
       'heavy_rain': '-1', 'sprinkles': '-1', 'numerous_showers': '-1', 'icy_mix': '-1', 'snow_showers_early': '-1',
       'low_clouds': '0', 'snow_rain_mix': '-1', 'flood': '-1', 'isolated_tstorms': '-1', 'light_rain_early': '-1',
       'light_snow_early': '-1', 'tornado': '-1', 'light_rain': '-1', 'high_level_clouds': '1', 'rain': '-1',
       'scattered_showers': '-1', 'snow_showers_late': '-1', 'snow': '-1', 'snow_changing_to_an_icy_mix': '-1',
       'clear': '1', 'overcast': '0', 'mostly_sunny': '1', 'heavy_mixture_of_precip': '-1',
       'rain_changing_to_an_icy_mix': '-1', 'snow_late': '-1', 'partly_sunny': '1', 'a_few_tstorms': '-1',
       'thunderstorms': '-1'}


def weather(p=['40.7128, -74.0059']):
    r_c = requests.request('get', 'https://reverse.geocoder.cit.api.here.com/6.2/reversegeocode.json',
                           params={'app_id': ['vbmECPJZjFd55Qjd2JhU'],
                                   'app_code': ['V17J9DdXQTuSDAWiFyH2vg'],
                                   'prox': p,
                                   'mode': ['retrieveLandmarks'],
                                   'gen': ['8']}
                           )

    res_c = json.loads(r_c.text)
    city = str(res_c['Response']['View'][0]['Result'][0]['Location']['Address']['City'])

    r = requests.request('get', 'https://weather.cit.api.here.com/weather/1.0/report.json',
                        params={'app_id': ['vbmECPJZjFd55Qjd2JhU'],
                                   'app_code': ['V17J9DdXQTuSDAWiFyH2vg'],
                        'product': ['observation'], 'name': city}
                        )
    icon = None
    text = json.loads(r.text)
    print json.dumps(text, indent=4)
    for i in range(len(text['observations']['location'])):
        if text['observations']['location'][i]['observation'][0]['city'] == city:
            icon = text['observations']['location'][i]['observation'][0]['iconName']
    if icon is not None:
        if icon in des.keys():
            return des[icon]
        else:
            return None
    else:
        return None

if __name__ == '__main__':
    weather()

