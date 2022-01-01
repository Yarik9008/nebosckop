import socket
import json
import cv2
import sqlite3


DB = 'data.sqlite3'

connect = sqlite3.connect(DB)
cursor = connect.cursor()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('0.0.0.0', 9090)
sock.bind(server_address)

sock.listen(1)
while True:
    connection, client_address = sock.accept()
    try:
        while True:
            data = connection.recv(1000)
            if data.decode() == '/end':
                print('Конец данных от:', client_address)
                break
            elif data.decode() == '/history':
                print('/history')
                ret = dict()
                ret['temp'] = cursor.execute('''SELECT * FROM temp ORDER BY date DESC LIMIT 200''').fetchall()
                ret['pressure'] = cursor.execute('''SELECT * FROM pressure ORDER BY date DESC LIMIT 200''').fetchall()
                ret['humidity'] = cursor.execute('''SELECT * FROM humidity ORDER BY date DESC LIMIT 200''').fetchall()
                ret['wind'] = cursor.execute('''SELECT * FROM wind ORDER BY date DESC LIMIT 200''').fetchall()
                connection.send(bytes(json.dumps(ret), 'utf-8'))

            elif data.decode() == '/data':
                print('/data')
                ret = dict()
                ret['temp'] = cursor.execute('''SELECT * FROM temp ORDER BY date DESC LIMIT 1''').fetchone()[0]
                ret['pressure'] = cursor.execute('''SELECT * FROM pressure ORDER BY date DESC LIMIT 1''').fetchone()[0]
                ret['humidity'] = cursor.execute('''SELECT * FROM humidity ORDER BY date DESC LIMIT 1''').fetchone()[0]
                ret['wind'] = cursor.execute('''SELECT * FROM wind ORDER BY date DESC LIMIT 1''').fetchone()[0]
                connection.send(bytes(json.dumps(ret), 'utf-8'))

            elif data.decode() == '/photo':
                print('/photo')
                cam = cv2.VideoCapture(0)
                grabbed, frame = cam.read()
                cam.release()
                if grabbed:
                    connection.send(frame.tobytes())
                else:
                    connection.send(b'error')
            elif data.decode() == '/satellite':
                print('/satellite')
                frame = cv2.imread('FY3B_2021-08-25_135058_VIRR-RGB-221-EQU.png', 0)
                connection.send(frame.tobytes())
    finally:
        connection.close()
