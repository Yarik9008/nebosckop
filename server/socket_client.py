import socket
import json
import dateutil
import matplotlib.pyplot as plt

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

socket.connect(('192.168.0.101', 9090))
socket.send(b'/history')
r = socket.recv(100000)
socket.send(b'/end')
socket.close()
print(r)
r = json.loads(r)
x_temp = []
y_temp = []
for i in r['temp']:
    x_temp.append(dateutil.parser.parse(i[1]))
    y_temp.append(i[0])
x_pressure = []
y_pressure = []
for i in r['pressure']:
    x_pressure.append(dateutil.parser.parse(i[1]))
    y_pressure.append(i[0])
x_humidity = []
y_humidity = []
for i in r['humidity']:
    x_humidity.append(dateutil.parser.parse(i[1]))
    y_humidity.append(i[0])
x_wind = []
y_wind = []
for i in r['wind']:
    x_wind.append(dateutil.parser.parse(i[1]))
    y_wind.append(i[0])
plt.plot(x_temp, y_temp)
#plt.plot(x_pressure, y_pressure)
plt.plot(x_humidity, y_humidity)
plt.plot(x_wind, y_wind)
plt.show()
