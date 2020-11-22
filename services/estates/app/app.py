#!/usr/bin/env python3

import asyncio, uvloop
import aiohttp.web
import aiohttp_jinja2 as jinja2 
import hashlib
import os
import random
import sqlite3
import time

from jinja2 import FileSystemLoader

BASE_DIR = os.path.dirname(__file__)
STATIC_DIR = os.path.join(BASE_DIR, 'static')

RB = str(random.getrandbits(1441))

create_db = not os.path.exists("/data/data.db")
db = sqlite3.connect("/data/data.db")
def q(query, *args, **kwargs):
    cur = db.cursor()
    try:
        cur.execute(query, *args, **kwargs)
        data = cur.fetchall()
        db.commit()
        return data
    except:
        db.rollback()

if create_db:
    q("CREATE TABLE users (user_id INTEGER, username TEXT, name TEXT, description TEXT, password_hash TEXT)")
    q("CREATE TABLE urts (id INTEGER, description TEXT)")
    q("CREATE TABLE participations (user_id INTEGER, urt_id INTEGER)")

def get_user(request):
    cookie = request.cookies.get("urtlogin", "")
    try:
        d, s = cookie.split(" ")
        if hashlib.sha1((d + RB).encode()).hexdigest() != s:
            return {i for i in range(0)}
        return {int(i) for i in d.split(",")}
    except:
        return {i for i in range(0)}

def get_user_str(user):
    return str(sum(user)) + " " + hashlib.sha1((str(sum(user)) + RB).encode()).hexdigest()

def build_app():
    app = aiohttp.web.Application()
    routes = aiohttp.web.RouteTableDef()

    @routes.get('/')
    async def root(request):
        user = get_user(request)
        return jinja2.render_template('index.html', request, {})

    @routes.post('/register')
    async def register(request):
        form = await request.post()
        q("""INSERT INTO users (user_id, username, name, description, password_hash) VALUES
             (1 + COALESCE((SELECT MAX(user_id) FROM users), 0), ?, ?, ?, ?)""",
         (form.get("username", ""), form.get("name", ""), form.get("description", ""),
          hashlib.sha1(form.get("password", "").encode()).hexdigest()))
        resp = aiohttp.web.HTTPFound("/")
        return jinja2.render_template('error.html', request, {"type": "reg-ok"})

    @routes.post('/login')
    async def login(request):
        user = get_user(request)
        form = await request.post()
        user_id = q("SELECT user_id FROM users WHERE username=? AND password_hash=?",
                    (form.get("username", ""), hashlib.sha1(form.get("password", "").encode()).hexdigest()))
        if user_id:
            user.add(user_id[0][0]) 
            resp = aiohttp.web.HTTPFound("/")
            resp.set_cookie("urtlogin", get_user_str(user))
            return resp
        else:
            return jinja2.render_template('error.html', request, {"type": "wrong-login"})

    @routes.post('/logout')
    async def logout(request):
        user = get_user(request)
        form = await request.post()

        resp = aiohttp.web.HTTPFound("/")
        resp.del_cookie("urtlogin")
        return resp

    @routes.get('/urt/random')
    async def random_urt(request):
        user = get_user(request)
        if not user:
            return jinja2.render_template("error.html", request, {"type": "unauth"})

        choices = [a for a, in q("SELECT id FROM urts")]
        choice = choices[int(hashlib.sha1((repr(user) + repr(int(time.time() / 60))).encode()).hexdigest(), 16) % len(choices)]
        resp = aiohttp.web.HTTPFound("/urt/" + str(choice))
        return resp

    @routes.get('/urt/{urt_id}')
    async def urt(request):
        user = get_user(request)
        if not user:
            return jinja2.render_template("error.html", request, {"type": "unauth"})

        urt_id = int(request.match_info["urt_id"])
        data = q("SELECT description FROM urts WHERE id=?", (urt_id, ))
        if not data:
            return jinja2.render_template("error.html", request, {"type": "urt-not-found"})

        users = q("SELECT u.user_id, u.name FROM participations AS p JOIN users AS u ON u.user_id = p.user_id WHERE p.urt_id = ?",
                  (urt_id, ))

        return jinja2.render_template("urt.html", request, {"id": urt_id, "description": data[0][0],
                                                            "users": users})

    @routes.post('/urt/join/{urt_id}')
    async def join_urt(request):
        user = get_user(request)
        if not user:
            return jinja2.render_template("error.html", request, {"type": "unauth"})
        urt_id = int(request.match_info["urt_id"])
        form = await request.post()

        if urt_id == 0:
            d = q("SELECT MAX(id) FROM urts")
            if d:
                max_urt_id = d[0][0]
            else:
                max_urt_id = 0
            t = int(time.time())
            if t != max_urt_id:
                q("INSERT INTO urts (id, description) VALUES (?, ?)", (t, form.get("description", "")))
                q("INSERT INTO participations (user_id, urt_id) VALUES (?, ?)", (max(user), t))
                resp = aiohttp.web.HTTPFound("/urt/" + str(t))
                return resp
            else:
                return jinja2.render_template("error.html", request, {"type": "many-urts"})
        else:
            if q("SELECT COUNT(*) FROM participations WHERE user_id=?", (max(user), ))[0][0] < 3:
                q("INSERT INTO participations (user_id, urt_id) VALUES (?, ?)", (max(user), urt_id))
                resp = aiohttp.web.HTTPFound("/urt/" + str(urt_id))
                return resp
            else:
                return jinja2.render_template("error.html", request, {"type": "many-participations"})

    @routes.get('/user/{user_id}')
    async def user_page(request):
        user = get_user(request)
        if not user:
            return jinja2.render_template("error.html", request, {"type": "unauth"})
        user_id = int(request.match_info["user_id"])

        data = q("SELECT username, name, description FROM users WHERE user_id=?", (user_id, ))
        if data:
            username, name, description = data[0]
            participations = [a for a, in q("SELECT urt_id FROM participations WHERE user_id=?", (user_id, ))]
            return jinja2.render_template('user.html', request,
                                          {"username": username, "name": name,
                                           "description": description if user_id in user else None,
                                           "participations": participations if user_id in user else None})
        else:
            return jinja2.render_template('error.html', request, {"type": "wrong-user"})

    routes.static('/static', STATIC_DIR)

    app.add_routes(routes)
    jinja2.setup(app, loader=FileSystemLoader(os.path.join(BASE_DIR, 'templates')))
    return app


if __name__ == "__main__":
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.get_event_loop()

    app = build_app()

    aiohttp.web.run_app(app, port=9009)
