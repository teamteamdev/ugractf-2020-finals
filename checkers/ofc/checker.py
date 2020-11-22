#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64
import json
import logging
import math
import string
import random
import re
import socket
import sys
import zlib


import requests

from adchecklib import BaseChecker, OK, Corrupt, Down, SetFlagId

sys.setrecursionlimit(1000000)


def solve(a, b):
    if a == 0:
        return (0, 1)

    x, y = solve(b % a, a)

    x, y = y - (b // a) * x, x

    while x < 0:
        x += b
        y -= a

    return (x, y)


def inverse(a, n):
    x, y = solve(a, n)
    return x


def sign(publickey, privatekey, val):
    modulo = int(publickey['modulo'])

    while True:
        onetime = random.randint(2, modulo - 2)
        if math.gcd(onetime, modulo - 1) == 1:
            break

    base = int(publickey['base'])
    high = pow(base, onetime, modulo)

    exponent = int(privatekey['exponent'])

    low = val - exponent * high
    inv = inverse(onetime, modulo - 1)
    low = (low * inv) % (modulo - 1)
    if low < 0:
        low += modulo - 1

    return (high, low)


class OfcChecker(BaseChecker):
    def rnd_num(self):
        return ''.join(random.choice(string.digits) for _ in range(13))

    def rnd_token(self):
        return ''.join(random.choice(string.digits + string.ascii_lowercase) for _ in range(13))

    def _assert(self, expr, exception=Down, message=''):
        if not expr:
            self.logger.error('Failed during assertion: %s', message)
            raise exception(message)

    def __init__(self):
        # vuln 1: flag in hidden field
        # vuln 2: flag in private key
        super().__init__(vulns=[2, 1])

    async def put(self, host, flag_id, flag, vuln):
        try:
            num = self.rnd_num()
            desc = self.rnd_token()

            s = requests.Session()
            r = s.post(f'http://{host}:8600/secureApplyPage', data={
                'enum': num, 
                'codeword': flag if vuln == "1" else desc
            })

            text = r.text

            if vuln == "1":
                self._assert(flag in text, Down, 'No codeword in profile.')
            else:
                self._assert(desc in text, Down, 'No codeword in profile.')

            r = s.post(f'http://{host}:8600/securePkiPage', data={
                'password': self.rnd_token() if vuln == "1" else flag
            })

            content = r.text
            content = '\n'.join(content.splitlines()[:2])

            compressed = base64.b64encode(zlib.compress(content.encode())).decode()

            raise SetFlagId(compressed)
        except (socket.timeout, requests.RequestException) as e:
            raise Down(f"Service is down: {type(e)}")

    async def get(self, host, flag_id, flag, vuln):
        try:
            s = requests.Session()
            r = s.get(f'http://{host}:8600/secureLoginChallenge')

            try:
                secret = re.findall('<pre>([\\d,]+)<', r.text)[0]
            except KeyError:
                raise Down("No one-time code")

            secret = int(secret.replace(',', ''))
            str_public_key, private_key = zlib.decompress(base64.b64decode(flag_id)).decode().splitlines()
            str_public_key = str_public_key.strip()
            public_key = json.loads(str_public_key)
            private_key = json.loads(private_key)
            high, low = sign(public_key, private_key, secret)

            r = s.post(f'http://{host}:8600/secureLoginChallenge', data={
                'key': str_public_key,
                'high': str(high),
                'low': str(low)
            })

            self._assert(
                str(public_key['enum']) in r.text,
                Corrupt,
                "No profile."
            )
            if vuln == "1":
                self._assert(
                    flag in r.text,
                    Corrupt,
                    "No flag."
                )
            
            r = requests.get(f'http://{host}:8600/recent')
            self._assert(
                str(public_key['enum']) in r.text,
                Corrupt,
                "Bad response for recent."
            )

            raise OK
        except (socket.timeout, requests.RequestException) as e:
            raise Down(f"Service is down: {type(e)}")

    async def check(self, host):
        raise OK

OfcChecker().run()
