import csv
import os.path
from random import *

OBJ_FACTOR = 'music_factor'
FILE_NAME = OBJ_FACTOR + '.csv'
ATTRS = ['Sound', 'Weather', 'Traffic', 'Speed', 'Luminucity', OBJ_FACTOR]

if os.path.isfile(FILE_NAME):
    print "Detected %s" %(FILE_NAME)
    f = open(FILE_NAME,'ab')
    writer = csv.writer(f)
else:
    # No such file exists
    print "%s does not exist. Create a new one." %(FILE_NAME)
    f = open(FILE_NAME, 'wb')
    writer = csv.writer(f)
    writer.writerow(ATTRS)

ctr = 0
print "Start generating training data..."

try:
    while True:
        # Ways to generate random number:
        #   1. random(): A random number in [0,1)
        #   2. randrange(a,b): A random number in [a,b)
        #   3. randint(a,b): A random integer in [a,b]
        sound =  random()
        weather = random()
        traffic = random()
        speed = random()
        luminous = random()
        output = input("[Data #%d]\n%s:%f  %s:%f  %s:%f  %s:%f  %s:%f \n Type your prediction of %s (value should be an integer in [0,100]) "
                        %(ctr, ATTRS[0], sound, ATTRS[1], weather,
                        ATTRS[2], traffic, ATTRS[3], speed,
                        ATTRS[4], luminous, OBJ_FACTOR)
                    )
        if not isinstance(output, int) or output < 0 or output > 100:
            print "Invalid format, try again."
            continue
        data = [sound, weather, traffic, speed, luminous, output/100.0]
        writer.writerow(data)
        ctr += 1
        print '\n'
except KeyboardInterrupt:
    f.close()
    print "\nExiting the program..."
