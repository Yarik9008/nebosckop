'''
sudo pip install pynmea2

'''
import struct
import serial
import pynmea2
def parseGPS(st):
    st = str(st)
    

    st = st[3:-5]
    
    if st.find('GGA') > 0:
        msg = pynmea2.parse(st)
        print (msg.timestamp,msg.lat,msg.lat_dir,msg.lon,msg.lon_dir,msg.altitude,msg.altitude_units)

serialPort = serial.Serial("/dev/ttyS0", 9600, timeout=0.5)
while True:
    st = serialPort.readline()
    parseGPS(st)