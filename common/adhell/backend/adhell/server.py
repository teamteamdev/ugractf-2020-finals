#!/usr/bin/env python3

import pathlib

import flask

from adhell import routes, utils


def create_app(config):
    app = flask.Flask(
        __name__,
        template_folder=pathlib.Path(__file__).parents[0] / 'templates'
    )
    app.config.from_mapping(config)

    utils.enhance_routing(app)
    utils.install_database(app, config['DATABASE_URL'])

    app.add_route('/api/me', routes.get_info, methods=['GET'])

    app.add_route('/api/payout', routes.payout, methods=['POST'])

    app.add_route('/api/transfers', routes.new_transfer, methods=['POST'])
    app.add_route('/api/transfers/<int:pk>', routes.accept_transfer, methods=['POST'])

    app.add_route('/api/banners', routes.new_banner, methods=['POST'])
    app.add_route('/api/banners/<int:pk>', routes.delete_banner, methods=['DELETE'])

    app.add_route('/ad/renderProduction.js', routes.get_banner)

    return app


def main():
    app = create_app(utils.get_config())
    app.run(port=7000, debug=True)
