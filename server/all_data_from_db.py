import sqlite3
import matplotlib.pyplot as plt
import dateutil
conn = sqlite3.connect('data.sqlite3')
cur = conn.cursor()
data = cur.execute('SELECT * FROM temp').fetchall()
x, y = [], []
for i in data:
    x.append(dateutil.parser.parse(i[1]))
    y.append(i[0])
print(x)
print(y)
'''
fig, ax = plt.subplots()
ax.plot(x, y)
'''
plt.plot(x, y)
plt.show()