import mraa  
  
def getGPS():  
    u = mraa.Uart(0)  
    u.setBaudRate(9600)  
    print u.getDevicePath()  
    status="V" 
    while (status!="A"):  
      if(u.dataAvailable()):  
           buff = u.readStr(256) 
           if(buff.find("GPRMC")!=-1):
               #print buff
               trimbuff=buff[buff.find("GPRMC"):-1]
               splitbuff=trimbuff.strip().split(',')
               #print trimbuff
               #print splitbuff
               if(len(splitbuff)<8):
                   continue
               status=splitbuff[2]
               latnmea=splitbuff[3]
               latdir=splitbuff[4]
               lonnmea=splitbuff[5]
               londir=splitbuff[6]
               speed=splitbuff[7]

    lat = float(latnmea[0:2]) + float(latnmea[2:])/60  
    lon = float(lonnmea[0:3]) + float(lonnmea[3:])/60
    spd = float(speed)*1.852
    if(latdir=="S"):
        lat*=-1
    if(londir=="W"):
        lon*=-1

    return [lat,lon,spd]
