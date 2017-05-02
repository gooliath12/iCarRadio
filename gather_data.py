import boto, json
from conn_aws import kinesis
# import light_sensor,traffic, weather

KINESIS_STREAM_NAME = 'iCarRadio'
# kinesis.put_record("as3",json.dumps(t),'0')
# The third parameter partition_key -- Specify which shard should use

# Generate Random data for test purpose
from random import *
# sound =  random()
# gpsdatas=gps.getgps()
# lan=gpsdatas[0]
# lon=gpsdatas[1]
# speed=gpsdata[2]
# weather = weather.weather([lan,lon])
# traffic = traffic.traffic()
# luminous = light_sensor.get_light()

# Test Data
tod = 'morning'
weather = 1
traffic = 5.0
speed = 80
luminous = 5


# Generate .JSON file
data = {
    "Time of Day": str(tod),
    "Weather": str(weather),
    "Traffic Condition": str(traffic),
    "Speed": str(speed),
    "Luminucity": str(luminous)
}

print json.dumps(data, indent=4)
kinesis.put_record(KINESIS_STREAM_NAME, json.dumps(data), 'shardId-000000000000')
