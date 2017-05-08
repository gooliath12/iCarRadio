import boto, json, datetime, time
from conn_aws import kinesis
import trafficAPI, weatherAPI2, lightSensor, gprmc
# import trafficAPI, weatherAPI2

KINESIS_STREAM_NAME = 'iCarRadio'


def get_tod():
    """
    Get time of day,
    Return time interval.
    """
    import datetime
    t1 = 16200  # 4:30
    t2 = 34200  # 8:30
    t3 = 63000  # 17:30
    t4 = 73800  # 20:30
    t5 = 82800  # 23:00
    now = datetime.datetime.now()
    bod = now.replace(hour=0, minute=0, second=0, microsecond=0)
    t = (now - bod).total_seconds()
    
    if t > t1 and t <= t2:  # 4:30 -- 9:30
        return 'morning'
    if t > t2 and t <= t3:  # 9:30 -- 17:30
        return 'mid-day'
    if t > t3 and t <= t4:  # 17:30 -- 20:30
        return 'off-work'
    if t > t4 and t <= t5:  # 20:30 -- 23:00
        return 'night'
    return 'midnight'  # 23:00 -- 4:30
    

def get_data():
    """
    Invoke all sensors & APIs, return a dict of data.
    """
    # # get data from sensors
    # gpsdatas=gprmc.getGPS()
    # lat=gpsdatas[0]
    # lng=gpsdatas[1]
    # speed=gpsdatas[2]
    # weather = weatherAPI2.weather(lat,lng)
    #weather=0
    # traffic = trafficAPI.getTraffic([str(lat)+","+str(lng)+","+"1"])
    # luminous = lightSensor.getLight()
    # check reasonable data range
    while True:
        
        # GPS: lat, lng % speed
        gpsdatas = gprmc.getGPS()
        lat = gpsdatas[0]
        lng = gpsdatas[1]
        speed = gpsdatas[2]
        # lat = 40.7128
        # lng = -74.0059
        # speed = 90

        # Light sensor
        luminous = lightSensor.getLight()
        # luminous = 5

        # Traffic and Weather APIs
        weather = weatherAPI2.weather(lat,lng)
        traffic = trafficAPI.getTraffic([str(lat)+","+str(lng)+","+"1"])
        
        if (-90<=lat<=90 and -180<=lng<=180 and 0<=speed<=140 and -1<=weather<=1 and 0<=traffic<=10 and 0<=luminous<=60):
            break
        else:
            print [luminous, weather, traffic, speed, lat, lng]
            print "Invalid data. Detect again."
            time.sleep(2)

    # Test Data
    #tod = 'morning'
    #weather = 1
    #traffic = 1.2
    #speed = 100
    #luminous = 7


    # Generate .JSON file
    data = {
	    "Time of Day": get_tod(),
        "Weather": str(weather),
        "Traffic": str(traffic),
        "Speed": str(speed),
        "Luminucity": str(luminous)
    }
    # print [luminous, weather, traffic, speed, lat, lng]
    #print json.dumps(data, indent=4)
    return data


def push_to_kinesis(data):
    kinesis.put_record(KINESIS_STREAM_NAME, json.dumps(data), 'shardId-000000000000')
    return None


if __name__ == '__main__':
    data = get_data()
    print json.dumps(data, indent=4)

