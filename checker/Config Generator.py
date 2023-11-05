import datetime
import os
import random
import sqlite3 as sqlite
import argparse
parser = argparse.ArgumentParser(description='Adding config openvpn')
parser.add_argument('nick', type=str, help='name')
parser.add_argument('days', type=str, help='days')
args = parser.parse_args()

def randomize(src):
    x=""
    for i in range(5):
        x+=str(random.randint(0,9))
    return src+"_"+x
def create_client():
    now_d=datetime.datetime.now()
    name=randomize(args.nick)
    days=args.days
    db = sqlite.connect('checker/base.db')
    cur = db.cursor()
    d=str(now_d.year)[-2:]+"-"+str(now_d.month)+"-"+str(now_d.day)
    cur.execute(f"INSERT INTO clients (s_date, name, days) VALUES ('{d}', '{name}', {days})")
    db.commit()
    os.system(f"bash checker/generate_cl.sh {name}")
    location="/root"
    file=location+"/"+name+".ovpn"
    print(file)
create_client()
