import functools
import os
import random
import string
import types

import flask
import yaml

from sqlalchemy import create_engine, orm

import adhell.models as models


def enhance_routing(app):
    def add_route(self, rule, func, **options):
        self.add_url_rule(
            rule,
            func.__name__,
            lambda *args, **kwargs: func(self, *args, **kwargs),
            **options
        )

    app.add_route = types.MethodType(add_route, app)


def create_database(db_engine):
    def inner():
        models.Base.metadata.create_all(db_engine)
    return inner


def remove_session(db):
    def inner(_=None):
        db.remove()
    return inner


def install_database(app, url):
    db_engine = create_engine(url, echo=True)
    db_factory = orm.sessionmaker(bind=db_engine)
    db = orm.scoped_session(db_factory)
    app.db = db

    app.before_first_request(create_database(db_engine))
    app.teardown_request(remove_session(db))


def get_config():
    with open(os.environ.get('CONFIG', 'config.yaml')) as config_file:
        return yaml.safe_load(config_file)


def authenticate_user(preload=False):
    def decorator(view):
        @functools.wraps(view)
        def inner(app, *args, **kwargs):
            remote_addr = flask.request.headers.get('X-Real-IP', flask.request.remote_addr)

            partner = app.db.query(models.Partner)

            if preload:
                partner = (partner
                           .options(
                               orm.joinedload(models.Partner.banners),
                               orm
                                .joinedload(models.Partner.incoming_transfers)
                                .joinedload(models.Transfer.sender)
                           ))

            try:
                partner = partner.filter(models.Partner.ip == remote_addr).one()
            except orm.exc.NoResultFound:
                return f"{remote_addr}: adhell@teamteam.dev to connect to our partner network!", 403

            return view(app, partner=partner, *args, **kwargs)

        return inner
    return decorator


def get_html_id():
    return random.choice(string.ascii_letters) + ''.join(
        random.choice(string.digits + string.ascii_letters)
        for _ in range(19)
    )
