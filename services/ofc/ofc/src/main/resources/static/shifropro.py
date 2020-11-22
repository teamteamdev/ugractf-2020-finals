#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import json
import random
import sys


sys.setrecursionlimit(1000000)


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


if len(sys.argv) != 2:
    print("Usage: shifropro.py keyfile")
    sys.exit(1)

with open(sys.argv[1], "r") as keyfile:
    rawpk = keyfile.readline()
    publickey = json.loads(rawpk)
    privatekey = json.loads(keyfile.readline())

print("SHIFROPRO 1.44")
print("Open Authorization from ofc.ru")
print("Please enter auth-token:::")

message = int(input().replace(',',''))

print("Please enter password")

password = input()

if password != privatekey["codeword"]:
    print("Bad password")
    sys.exit(1)

modulo = int(publickey['modulo'])

while True:
    onetime = random.randint(2, modulo - 2)
    if math.gcd(onetime, modulo - 1) == 1:
        break

base = int(publickey['base'])
high = pow(base, onetime, modulo)

exponent = int(privatekey['exponent'])

low = message - exponent * high
inv = inverse(onetime, modulo - 1)
low = (low * inv) % (modulo - 1)
if low < 0:
    low += modulo - 1

print("SUCCESS!!!!")
print("Public key:", rawpk)
print("High signature:", high)
print("Low signature:", low)
print()
print("Thank you for using ShifroPro")

print("(c) Shifro Corp. 2012")
