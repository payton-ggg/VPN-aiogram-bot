import datetime
import os
import sqlite3 as sqlite
import time
while True:
    db = sqlite.connect('base.db')
    cur = db.cursor()
    cur.execute(f"SELECT * FROM clients")
    now_d=datetime.datetime.now()
    r=cur.fetchall()
    for i in range(len(r)):
        start_d=datetime.datetime.strptime(r[i][0], '%y-%m-%d')+datetime.timedelta(days=r[i][2])
        name=r[i][1]
        print(start_d)
        if now_d>=start_d:
            print(f"{name} outdated")
            cur.execute('''DELETE FROM clients WHERE name = ?''', (name,))
            db.commit()
            os.system(f"bash revoke_cl.sh {name}")
    db.close()
    time.sleep(((0.5*60)*60)*24)