from adchecklib import BaseChecker, OK, Corrupt, Down, CheckerException, SetFlagId

import requests
import hashlib


class MyChecker(BaseChecker):
    def __init__(self):
        super().__init__(vulns=[1, 1])

    def password_for(self, user):
        return hashlib.sha1((user + "3420v3nb0a9enb0ne0ab43nt243r029130----").encode()).hexdigest()        
        
    async def put(self, host, flag_id, flag, vuln):
        try:
            requests.post("http://%s:9009/register" % host,
                          data={"username": flag_id,
                                "password": self.password_for(flag_id),
                                "description": flag if vuln == "2" else "", "name": flag_id})
            if vuln == "1":  # urt data
                s = requests.Session()
                s.post("http://%s:9009/login" % host,
                       data={"username": flag_id, "password": self.password_for(flag_id)})
                resp = s.post("http://%s:9009/urt/join/0" % host, data={"description": flag}, allow_redirects=False)
                if resp.status_code not in {302, 301, 303}:
                    raise Down("No redirect after urt creation")
                urt_id = resp.headers["Location"].split("/")[-1]
                raise SetFlagId(flag_id + " " + urt_id)
            elif vuln == "2":  # user data
                raise OK
        except CheckerException:
            raise
        except Exception as e:
            raise Down(str(e))

    async def get(self, host, flag_id, flag, vuln):
        try:
            s = requests.Session()
            resp = s.post("http://%s:9009/login" % host,
                          data={"username": flag_id.split(" ")[0],
                                "password": self.password_for(flag_id.split(" ")[0])})
            if "urtlogin" not in s.cookies:
                raise Corrupt("Unable to log in to the service")

            if vuln == "1":  # urt data
                urt_id = int(flag_id.split(" ")[1])
                text = s.get("http://%s:9009/urt/%d" % (host, urt_id)).text
            elif vuln == "2":  # user data
                user_id = int(s.cookies["urtlogin"].strip('"').split(" ")[0])
                text = s.get("http://%s:9009/user/%d" % (host, user_id)).text

            if flag in text:
                raise OK
            else:
                raise Corrupt("Unable to retrieve flag")
        except CheckerException:
            raise
        except Exception as e:
            raise Down(str(e))

    async def check(self, host):
        try:
            requests.get("http://%s:9009/" % host)
            raise OK
        except CheckerException:
            raise
        except Exception as e:
            raise Down(str(e))

MyChecker().run()

