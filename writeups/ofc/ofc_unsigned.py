#!/usr/bin/env python3

import copy
import json
import math
import random
import re
import sys

import requests

MY_PRIVATE = {"base":"65230961056","modulo":"68529649687","result":"67587995761","exponent":"3734510131","codeword":"1337133713371"}
MY_PUBLIC = {"base":"65230961056","modulo":"68529649687","result":"67587995761","enum":"1337133713371","signatureHigh":"42638038611637582796718971786323838681652897472603035443794749058969805563415016603090288379578296494965621113606778587981895254575896714000597931211632124707660422163615551328436285227862323595294986834162847384073817546926376727806938487442212739861211613793164206502032070496977372923745115937379339675382","signatureLow":"93982390612154192090646092374827845356564504843339898443927192977982398299295190635177146542277857201206222959814625259536389943349041336795517321275390179161786963802682354644185412448124425823471241998336595338631466327374699669987902999100463310285400064776483505980740214863747090303291649207662670353267"}

ip = sys.argv[1]

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

r = requests.get(f"http://{ip}:8600/recent")
for user_id in re.findall(r'header">([0-9,]+)<', r.text):
    public = copy.copy(MY_PUBLIC)
    public["enum"] = user_id.replace(",", "")
    private = copy.copy(MY_PRIVATE)

    s = requests.Session()

    r = s.get(f"http://{ip}:8600/secureLoginChallenge")

    try:
        message, = re.findall('<pre>([0-9,]+)</pre>', r.text)
    except:
        continue

    message = int(message.replace(",", ""))

    modulo = int(public['modulo'])

    while True:
        onetime = random.randint(2, modulo - 2)
        if math.gcd(onetime, modulo - 1) == 1:
            break

    base = int(public['base'])
    high = pow(base, onetime, modulo)

    exponent = int(private['exponent'])

    low = message - exponent * high
    inv = inverse(onetime, modulo - 1)
    low = (low * inv) % (modulo - 1)
    if low < 0:
        low += modulo - 1

    r = s.post(
        f"http://{ip}:8600/secureLoginChallenge",
        data={
            "key": json.dumps(public),
            "high": str(high),
            "low": str(low)
        },
        allow_redirects=True
    )

    print(re.findall(r'black;">([^<]+)</strong', r.text), flush=True)
