import aiosqlite
import sqlite3
import os

db_path = os.path.join("users.db")

#Создание базы данных
def create_tables():
    with sqlite3.connect(db_path, check_same_thread=False) as conn:
        cur=conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users(userid INTEGER, balance INTEGER, act_promos STRING, inviter INTEGER, admin INTEGER, blocked INTEGER, api_key STRING);""")
        cur.execute("""CREATE TABLE IF NOT EXISTS payments(id INTEGER PRIMARY KEY AUTOINCREMENT, summ INTEGER, chatid INTEGER, location STRING);""")
        cur.execute("""CREATE TABLE IF NOT EXISTS promocodes(id INTEGER PRIMARY KEY AUTOINCREMENT, promocode STRING, summ INTEGER, act_count INTEGER);""")
        cur.execute("""CREATE TABLE IF NOT EXISTS servers(id INTEGER PRIMARY KEY AUTOINCREMENT, name STRING, ip STRING, user STRING, pass STRING);""")
        cur.execute("""CREATE TABLE IF NOT EXISTS config(onecfg_summ INTEGER);""")
        cur.close()
#Отчистка статистики
async def clear_stat():
    conn = await aiosqlite.connect(db_path, check_same_thread=False)
    cur = await conn.cursor()
    await cur.execute("DELETE from payments;")
    await conn.commit()
    await conn.close()
#Получение колличества всех юзеров
async def count_all_users():
    conn = await aiosqlite.connect(db_path, check_same_thread=False)
    cur = await conn.cursor()
    data = await cur.execute('SELECT COUNT(userid) FROM users')
    all = await data.fetchone()
    await conn.close()
    return all[0]
#Получение списка покупок
async def count_buys():
    conn = await aiosqlite.connect(db_path, check_same_thread=False)
    cur = await conn.cursor()
    data = await cur.execute('SELECT COUNT(id) FROM payments')
    buys = await data.fetchone()
    await conn.close()
    return buys[0]
#Получение списка покупок локации Москва
async def count_where_buys(loc):
    conn = await aiosqlite.connect(db_path, check_same_thread=False)
    cur = await conn.cursor()
    data = await cur.execute(f'SELECT COUNT(location) FROM payments WHERE location="{loc}"')
    msc_buys = await data.fetchone()
    await conn.close()
    return msc_buys[0]
#Получение суммы покупок
async def payments_summ():
    conn = await aiosqlite.connect(db_path, check_same_thread=False)
    cur = await conn.cursor()
    data = await cur.execute('SELECT summ FROM payments')
    payment_list = await data.fetchall()
    await conn.close()
    if payment_list != None:
        all_summ=0
        for i in payment_list:
            all_summ+=int(i[0])
        return str(all_summ)
    else:
        return "0"
#Получения всех юзерайди для рассылки
async def all_userids():
    conn = await aiosqlite.connect(db_path, check_same_thread=False)
    cur = await conn.cursor()
    data = await cur.execute('SELECT userid FROM users')
    resp = await data.fetchall()
    await conn.close()
    return resp
#Создание промокода
async def create_promo(promo, promosumm, act_cnt):
    conn = await aiosqlite.connect(db_path, check_same_thread=False)
    cur = await conn.cursor()
    await cur.execute("INSERT INTO promocodes VALUES(NULL,?,?,?);", (promo, promosumm, act_cnt))
    await conn.commit()
    await conn.close()
#Получение информации о пользователе
async def get_user_info(chatid):
    conn = await aiosqlite.connect(db_path, check_same_thread=False)
    cur = await conn.cursor()
    data = await cur.execute('SELECT * FROM users WHERE userid=?', (chatid,))
    usr_info= await data.fetchone()
    await conn.close()
    return usr_info
#Запись информации о пользователе в БД
async def save_user_info(chatid, inviter=0):
    conn = await aiosqlite.connect(db_path, check_same_thread=False)
    cur = await conn.cursor()
    if inviter == 0:
        user_data = (chatid,0,None)
        await cur.execute("INSERT INTO users VALUES(?,?,NULL,?,0,0,NULL);", user_data)
        await conn.commit()
    else:
        user_data = (chatid,0,inviter)
        await cur.execute("INSERT INTO users VALUES(?,?,NULL,?,0,0,NULL);", user_data)
        await conn.commit()
    await conn.close()
#Запись балана по юзерайди
async def write_balance(newbal, userid):
    conn = await aiosqlite.connect(db_path, check_same_thread=False)
    cur = await conn.cursor()
    await cur.execute(f"UPDATE users SET balance = {newbal} WHERE userid = {userid}")
    await conn.commit()
    await conn.close()
#Сохранение информации о платеже
async def write_payment_info(summ, userid, loc):
    conn = await aiosqlite.connect(db_path, check_same_thread=False)
    cur = await conn.cursor()
    await cur.execute(f"INSERT INTO payments VALUES(NULL,?,?,?);", (summ,userid,loc))
    await conn.commit()
    await conn.close()
#Получение инвайтера по юзерайди
async def get_inviter(userid):
    conn = await aiosqlite.connect(db_path, check_same_thread=False)
    cur = await conn.cursor()
    data = await cur.execute(f'SELECT inviter FROM users WHERE userid={userid}')
    inviter = await data.fetchone()
    await conn.close()
    return inviter[0]
#Информация о промокоде
async def get_promo_info(promo):
    conn = await aiosqlite.connect(db_path, check_same_thread=False)
    cur = await conn.cursor()
    req = await cur.execute(f'SELECT * FROM promocodes WHERE promocode="{promo}"')
    promoinfo = await req.fetchone()
    await conn.close()
    return promoinfo
#Список всех промокодов
async def get_all_promos():
    conn = await aiosqlite.connect(db_path, check_same_thread=False)
    cur = await conn.cursor()
    req = await cur.execute(f'SELECT * FROM promocodes')
    promoinfo = await req.fetchall()
    await conn.close()
    return promoinfo
#Удаление промокода
async def delete_promo(promo):
    conn = await aiosqlite.connect(db_path, check_same_thread=False)
    cur = await conn.cursor()
    await cur.execute(f'DELETE FROM promocodes WHERE promocode="{promo}"')
    await conn.commit()
    await conn.close()
#Обновлене активированных промиков
async def write_act_promos(pr, userid):
    conn = await aiosqlite.connect(db_path, check_same_thread=False)
    cur = await conn.cursor()
    await cur.execute(f"UPDATE users set act_promos = '{pr}' WHERE userid = '{userid}'")
    await conn.commit()
    await conn.close()
#Обновлене колличества активаций промокода
async def write_act_count(act_count, promo):
    conn = await aiosqlite.connect(db_path, check_same_thread=False)
    cur = await conn.cursor()
    await cur.execute(f"UPDATE promocodes SET act_count = '{act_count}' WHERE promocode = '{promo}'")
    await conn.commit()
    await conn.close()
#Изменение админки по id
async def set_admin(id, mode):
    conn = await aiosqlite.connect(db_path, check_same_thread=False)
    cur = await conn.cursor()
    await cur.execute(f"UPDATE users SET admin = '{mode}' WHERE userid = '{id}'")
    await conn.commit()
    await conn.close()
#Список админов
async def admin_list():
    conn = await aiosqlite.connect(db_path, check_same_thread=False)
    cur = await conn.cursor()
    req = await cur.execute(f"SELECT * FROM users WHERE admin=1")
    data = await req.fetchall()
    await conn.close()
    return data
#Забанить юзера
async def ban(userid, mode):
    conn = await aiosqlite.connect(db_path, check_same_thread=False)
    cur = await conn.cursor()
    await cur.execute(f"UPDATE users SET blocked = {mode} WHERE userid = '{userid}'")
    await conn.commit()
    await conn.close()
#Обновление и геренация апи ключа
async def update_key(userid, key = None):
    conn = await aiosqlite.connect(db_path, check_same_thread=False)
    cur = await conn.cursor()
    if key != None:
        await cur.execute(f"UPDATE users SET api_key = '{key}' WHERE userid = '{userid}'")
    else:
        await cur.execute(f"UPDATE users SET api_key = NULL WHERE userid = '{userid}'")
    await conn.commit()
    await conn.close()
#Список серверов
async def get_servers():
    conn = await aiosqlite.connect(db_path, check_same_thread=False)
    cur = await conn.cursor()
    req = await cur.execute("SELECT * FROM servers")
    servers = await req.fetchall()
    await conn.close()
    return servers
#Информация о конкретном сервере
async def get_server(id):
    conn = await aiosqlite.connect(db_path, check_same_thread=False)
    cur = await conn.cursor()
    req = await cur.execute("SELECT * FROM servers WHERE id=?", (id,))
    servers = await req.fetchall()
    await conn.close()
    return servers[0]
#Получение цены кфг из дб
async def get_one_summ():
    conn = await aiosqlite.connect(db_path, check_same_thread=False)
    cur = await conn.cursor()
    req = await cur.execute("SELECT onecfg_summ FROM config")
    settings = await req.fetchone()
    await conn.close()
    return settings[0]
#Устновка цены кфг в дб
async def set_price(price):
    conn = await aiosqlite.connect(db_path, check_same_thread=False)
    cur = await conn.cursor()
    await cur.execute(f"UPDATE config SET onecfg_summ={price} WHERE id = 1")
    await conn.commit()
    await conn.close()
#Удаление сервера из дб
async def delete_server(server):
    conn = await aiosqlite.connect(db_path, check_same_thread=False)
    cur = await conn.cursor()
    await cur.execute(f"DELETE FROM servers WHERE id={server}")
    await conn.commit()
    await conn.close()
#Добавление сервера в дб
async def add_server(name, ip, username, password):
    conn = await aiosqlite.connect(db_path, check_same_thread=False)
    cur = await conn.cursor()
    await cur.execute(f"INSERT INTO servers(name, ip, user, pass) VALUES(?,?,?,?)", (name, ip, username, password))
    await conn.commit()
    await conn.close()
