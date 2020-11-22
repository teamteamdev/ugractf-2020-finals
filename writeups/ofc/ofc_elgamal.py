#!/usr/bin/env python3

import json
import math
import random
import re
import sys

import requests

ip = sys.argv[1]

def solve(a: int, b: int):
    # find solution for ax + by == 1 that 0 < x < n

    if a == 0:
        return (0, 1)

    x, y = solve(b % a, a)

    x, y = y - (b // a) * x, x

    while x < 0:
        x += b
        y -= a

    return (x, y)


def inverse(a: int, n: int):
    # find x such that ax == 1 (mod n)

    x, y = solve(a, n)
    return x


# https://github.com/markusju/pollard-rho
def step(x: int, a: int, b: int, G: int, H: int, P: int, Q: int):
    sub = x % 3 # Subsets

    if sub == 0:
        x = x*G % P
        a = (a+1) % Q

    if sub == 1:
        x = x * H % P
        b = (b + 1) % Q

    if sub == 2:
        x = x*x % P
        a = a*2 % Q
        b = b*2 % Q

    return x, a, b


def verify(g, h, p, x):
    return pow(g, x, p) == h


def pollard(G: int, H: int, P: int):
    Q = (P - 1) // 2  # sub group


    x = G*H
    a = 1
    b = 1

    X = x
    A = a
    B = b

    for i in range(1, P):
        x, a, b = step(x, a, b, G, H, P, Q)

        X, A, B = step(X, A, B, G, H, P, Q)
        X, A, B = step(X, A, B, G, H, P, Q)

        if x == X:
            break


    nom = a-A
    denom = B-b

    while denom < 0:
        denom += Q

    res = (inverse(denom, Q) * nom) % Q

    if verify(G, H, P, res):
        return res

    return res + Q


recent = requests.get(f"http://{ip}:8600/recent")
for line in re.findall(r'code>([^<]+)</code', recent.text):
    key = json.loads(line)

    s = requests.Session()

    r = s.get(f"http://{ip}:8600/secureLoginChallenge")

    try:
        message, = re.findall('<pre>([0-9,]+)</pre>', r.text)
    except:
        continue

    message = int(message.replace(",", ""))

    modulo = int(key['modulo'])
    result = int(key['result'])

    while True:
        onetime = random.randint(2, modulo - 2)
        if math.gcd(onetime, modulo - 1) == 1:
            break

    base = int(key['base'])
    high = pow(base, onetime, modulo)

    exponent = pollard(base, result, modulo)

    low = message - exponent * high
    inv = inverse(onetime, modulo - 1)
    low = (low * inv) % (modulo - 1)
    if low < 0:
        low += modulo - 1

    r = s.post(
        f"http://{ip}:8600/secureLoginChallenge",
        data={
            "key": line,
            "high": str(high),
            "low": str(low)
        },
        allow_redirects=True
    )

    print(re.findall(r'black;">([^<]+)</strong', r.text), flush=True)
