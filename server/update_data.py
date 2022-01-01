import time
import random
import sqlite3
import datetime

SLEEP = 1
DB = 'data.sqlite3'

connect = sqlite3.connect(DB)
cursor = connect.cursor()


def delta_lim(value, delta, max, min):
    if value > max:
        return value - abs(delta)
    elif value < min:
        return value + abs(delta)
    else:
        return value + delta


def generate_values():
    # ------------- temp -------------------
    val = delta_lim(cursor.execute('''SELECT * FROM temp ORDER BY date DESC LIMIT 1''').fetchone()[0],
                    (random.randint(-100, 100) / 100), 40, -40)
    cursor.execute(
        f'''INSERT INTO temp (val, date) values ({round(val, 2)}, "{datetime.datetime.now().isoformat()}")''')
    connect.commit()
    print(f'temp: {val}')
    # ------------- pressure -------------------
    val = delta_lim(cursor.execute('''SELECT * FROM pressure ORDER BY date DESC LIMIT 1''').fetchone()[0],
                    (random.randint(-3, 3)), 1000, 500)
    cursor.execute(f'''INSERT INTO pressure (val, date) values ({val}, "{datetime.datetime.now().isoformat()}")''')
    connect.commit()
    print(f'pressure: {val}')
    # ------------- humidity -------------------
    val = delta_lim(cursor.execute('''SELECT * FROM humidity ORDER BY date DESC LIMIT 1''').fetchone()[0],
                    (random.randint(-100, 100) / 100), 100, 0)
    cursor.execute(
        f'''INSERT INTO humidity (val, date) values ({round(val, 2)}, "{datetime.datetime.now().isoformat()}")''')
    connect.commit()
    print(f'humidity: {val}')
    # ------------- wind -------------------
    val = delta_lim(cursor.execute('''SELECT * FROM wind ORDER BY date DESC LIMIT 1''').fetchone()[0],
                    (random.randint(-100, 100) / 100), 40, 0)
    cursor.execute(
        f'''INSERT INTO wind (val, date) values ({round(val, 2)}, "{datetime.datetime.now().isoformat()}")''')
    connect.commit()
    print(f'wind: {val}')


if __name__ == '__main__':
    while True:
        time.sleep(SLEEP)
        generate_values()
