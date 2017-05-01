import csv
import os.path
from random import *

# Optional music factors
# 1. energy
# 2. acousticness
# 3. danceability
# 4. valence
OBJ_FACTOR = 'music_factor'

# Optional Time of Day
# 1. morning
# 2. midday
# 3. off work
# 4. night
# 5. midnight
TOD = 'morning'

FILE_NAME = OBJ_FACTOR + '.csv'
ATTRS = [TOD, 'Weather', 'Traffic', 'Speed', 'Luminucity', OBJ_FACTOR]


def compute_speed(traffic, limit):
    """
    Compute speed according to the formula.
    """
    median = (limit*0.16) * (10-traffic)
    rng = 20
    if median - 20 < 0:
        return uniform(0, median+20)
    else:
        return uniform(median-20, median+20)

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
        # sound =  random()
        weather = randint(-1, 1)
        traffic = uniform(0, 10)
        limit = 80 if random()<0.5 else 120
        speed = compute_speed(traffic, limit)
        luminous = randint(0,10)
        output = input("[Data #%d]\n%s:%d  %s:%f  %s:%f  %s:%d \n Type your prediction of %s (value should be an integer in [0,100])"
                        %(ctr, ATTRS[1], weather, ATTRS[2], traffic, ATTRS[3], speed, ATTRS[4], luminous, OBJ_FACTOR)
                    )
        if not isinstance(output, int) or output < 0 or output > 100:
            print "Invalid format, try again."
            continue
        data = [TOD, weather, traffic, speed, luminous, output/100.0]
        writer.writerow(data)
        ctr += 1
        print '\n'
except KeyboardInterrupt:
    f.close()
    print "\nExiting the program..."
