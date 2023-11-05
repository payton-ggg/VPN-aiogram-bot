import string
import random
import paramiko
import os
from sys import platform
from scp import SCPClient

#Разделение баланса по рарядности
def beauty_int(ini):
    stri=int(ini)
    return f"{stri:_}".replace("_", " ")

#Очищение консоли
def clear():
    if platform == "linux" or platform == "linux2":
        os.system("clear")
    elif platform == "win32":
        os.system("cls")

#Генерация коммента для лолза
def comment_generation(id=0):
    cmnt=""
    for i in range(7):
            cmnt+=random.choice(string.ascii_letters)
    if id != 0:
        return str(id)+cmnt
    else:
        return cmnt
#Удаление файла
def delete(name):
    if os.path.isfile(name):
        os.remove(name)

# Генерация ключа апи
def generate_api_key():
    key=""
    for a in range(4):
        for b in range(7):
            key+=random.choice(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
        key+="-"
    return key[:-1]

#Генерация конфига
def generate_config(name: str, days: str, server_data: list):
    host = server_data[2]
    user = server_data[3]
    secret = server_data[4]
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user, password=secret, port=22)
    stdin, stdout, stderr = client.exec_command("python3 'checker/Config Generator.py' "+str(name)+" "+str(days))
    data = (stdout.read() + stderr.read()).decode().split("\n")[4]
    scp = SCPClient(client.get_transport())
    scp.get(data)
    client.close()
    scp.close()
    return data