import sys, json,random

light=random.randrange(0,10,1)
weather=random.randrange(-1,2,1)
traffic=random.random()*10
speed=random.random()*140
lat=(random.random()-0.5)*180
lon=(random.random()-0.5)*360


print [light,weather,traffic,speed,lat,lon]
