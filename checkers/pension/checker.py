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




class PensionChecker(BaseChecker):
    def rnd_num(self):
        return ''.join(random.choice(string.digits) for _ in range(13))

    def rnd_token(self):
        return ''.join(random.choice(string.digits + string.ascii_lowercase) for _ in range(13))

    def _assert(self, expr, exception=Down, message=''):
        if not expr:
            self.logger.error('Failed during assertion: %s', message)
            raise exception(message)

    def __init__(self):
        super().__init__()

    async def register_pensioner(self, host):
        try:
            passcode = str(self.rnd_num())

            s = requests.Session()
            r = s.get(f'http://{host}:3100/add-retiree')

            try:
                token = re.findall('type="hidden" value="([A-Za-z0-9._-]+)"', r.text)[0]
            except IndexError:
                raise Down("CSRF Failed")

            fn = self.rnd_token()

            r = s.post(f'http://{host}:3100/add-retiree', data={
                'first_name': fn,
                'last_name': self.rnd_token(),
                'csrf_token': token,
                'passcode': passcode,
                'date_of_birth': '19991201',
                'accept_tos': 'y'
            })

            try:
                return re.findall(f'(\\d+) {fn}', r.text)[0], passcode
            except IndexError:
                raise Down("Can't read the report add-retiree")
        except (socket.timeout, requests.RequestException) as e:
            raise Down(f"Can't register: service doesn't work: {type(e)}")


    async def put(self, host, flag_id, flag, vuln):
        try:
            pen_id, passcode = await self.register_pensioner(host)

            s = requests.Session()
            r = s.get(f'http://{host}:3100/add-paycheck')

            try:
                token = re.findall('type="hidden" value="([A-Za-z0-9._-]+)"', r.text)[0]
            except IndexError:
                raise Down("CSRF Failed")

            r = s.post(f'http://{host}:3100/add-paycheck', data={
                'retiree_id': pen_id,
                'csrf_token': token,
                'passcode': passcode,
                'date': '20201124',
                'amount': str(random.randint(1, 1000000)),
                'signature': flag
            })

            self._assert(
                '2020.11.24' in r.text,
                Down,
                "Can't read the report add-paycheck"
            )

            raise SetFlagId(f'{pen_id}:{passcode}')
        except (socket.timeout, requests.RequestException) as e:
            raise Down(f"Can't add check: doesn't work: {type(e)}")

    async def get(self, host, flag_id, flag, vuln):
        try:
            pen_id, passcode = flag_id.split(':')

            s = requests.Session()
            r = s.get(f'http://{host}:3100/show-paychecks')

            try:
                token = re.findall('type="hidden" value="([A-Za-z0-9._-]+)"', r.text)[0]
            except IndexError:
                raise Down("CSRF Failed")

            r = s.post(f'http://{host}:3100/show-paychecks', data={
                'retiree_id': pen_id,
                'csrf_token': token,
                'passcode': passcode
            })

            self._assert(
                flag[:31] in r.text,
                Corrupt,
                "Can't read the report show-paychecks"
            )

            raise OK
        except (socket.timeout, requests.RequestException) as e:
            raise Down(f"Can't show paychecks: doesn't work: {type(e)}")

    async def check(self, host):
        try:
            r = requests.get(f'http://{host}:3100/')
            self._assert(
                "РосМосГосКосмос" in r.text,
                Down,
                "Can't read main page"
            )

            pen_id, passcode = await self.register_pensioner(host)

            new_code = str(self.rnd_num())

            s = requests.Session()
            r = s.get(f'http://{host}:3100/change-passcode')

            try:
                token = re.findall('type="hidden" value="([A-Za-z0-9._-]+)"', r.text)[0]
            except IndexError:
                raise Down("CSRF Failed")

            r = s.post(f'http://{host}:3100/change-passcode', data={
                'retiree_id': pen_id,
                'csrf_token': token,
                'passcode': passcode,
                'new_passcode': new_code,
                'submit': 'ЗАПРОСИТЬ'
            })

            self._assert(
                pen_id in r.text,
                Down,
                "Can't read the report change-passcode"
            )

            raise OK
        except (socket.timeout, requests.RequestException) as e:
            self.logger.exception(e)
            raise Down(f"Can't change pass: doesn't work: {type(e)}")

PensionChecker().run()
