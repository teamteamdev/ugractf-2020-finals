import json
import math
import re

import cryptography.fernet as fernet
import flask

from sqlalchemy import orm, sql

from adhell import models, utils


def get_banner(app):
    query = sql.text('''
with
  bannercount as (
      select partner.id, count(banner.id) as banners from partner
      inner join banner on banner.owner_id = partner.id
      group by partner.id
      having count(banner.id) > 0
  ),
  p as (select *, balance::numeric / sum(balance) over () as prob from partner natural join bannercount),
  cp as (select *, sum(p.prob) over (order by prob desc rows between unbounded preceding and current row) as cumprob from p),
  fp as (select *, cumprob - prob as lastprob from cp),
  row as (
    select fp.* from fp
    cross join (select random()) as random(val)
    where fp.cumprob >= random.val
    limit 1
  )
select * from banner where owner_id = (select id from row)
offset floor(random() * (select banners from row))
limit 1;
''')

    banner = (app.db
              .query(models.Banner)
              .options(orm.joinedload(models.Banner.owner))
              .from_statement(query).one())
    
    html_id = utils.get_html_id()
    
    meta = json.dumps({
        'partner': banner.owner.ip == '10.2.0.20',
        'block': html_id,
        'format': banner.format,
        'content': banner.content
    })

    meta = fernet.Fernet(app.config['CHECKER_SECRET_KEY']).encrypt(meta.encode()).decode()

    referrer = re.findall(r'\d+\.\d+\.\d+\.\d+', flask.request.headers.get('Referer', ''))
    if referrer:
        try:
            partner = app.db.query(models.Partner).filter(models.Partner.ip == referrer[0]).one()
            partner.views += 1
            app.db.commit()
        except orm.exc.NoResultFound:
            pass

    return flask.Response(
        flask.render_template(f'{banner.format}.js', html_id=html_id, meta=meta, banner=banner),
        mimetype='text/javascript',
        headers={
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': '*',
            'Access-Control-Max-Age': '21600'
        }
    )


@utils.authenticate_user(preload=True)
def get_info(_, partner):
    return flask.jsonify({
        'id': partner.id,
        'ip': partner.ip,
        'name': partner.name,
        'balance': partner.balance,
        'views': partner.views,
        'banners': [
            {
                'id': banner.id,
                'name': banner.name,
                'format': banner.format,
                'content': banner.content
            }
            for banner in partner.banners
        ],
        'incoming_transfers': [
            {
                'id': transfer.id,
                'sender': transfer.sender.name,
                'amount': transfer.amount
            }
            for transfer in partner.incoming_transfers
            if not transfer.is_received
        ]
    })


@utils.authenticate_user()
def payout(app, partner):
    if partner.views < 1024:
        return flask.jsonify({
            'status': 'error',
            'message': 'You can payout 1024 views and more.'
        }), 400

    partner.balance += int(math.log(partner.views, 1024))
    partner.balance = partner.balance % 2048
    partner.views = 0
    app.db.commit()
    return flask.jsonify({'status': 'ok'})


@utils.authenticate_user()
def new_transfer(app, partner):
    data = flask.request.json

    try:
        receiver_id = data['receiver_id']
        assert isinstance(receiver_id, int)

        app.db.query(models.Partner).filter(models.Partner.id == receiver_id).one()

        amount = data['amount']
        assert isinstance(amount, int) and amount <= partner.balance
    except (AssertionError, KeyError, orm.exc.NoResultFound):
        return flask.jsonify({'status': 'error', 'message': 'Malformed API call.'}), 400

    transfer = models.Transfer(sender_id=partner.id, receiver_id=receiver_id, amount=amount)
    app.db.add(transfer)
    app.db.commit()

    return flask.jsonify({'status': 'ok'})


@utils.authenticate_user()
def accept_transfer(app, partner, pk):
    try:
        sender = orm.aliased(models.Partner)
        receiver = orm.aliased(models.Partner)

        transfer = (app.db.query(models.Transfer)
                    .join(sender, models.Transfer.sender)
                    .join(receiver, models.Transfer.receiver)
                    .options(
                        orm.contains_eager(models.Transfer.sender),
                        orm.contains_eager(models.Transfer.receiver)
                    )
                    .filter(
                        models.Transfer.id == pk,
                        models.Transfer.receiver_id == partner.id,
                        models.Transfer.is_received == False,
                        sender.balance >= models.Transfer.amount
                    )
                    .one())
    except orm.exc.NoResultFound:
        return flask.jsonify({'status': 'error', 'message': 'No transfer.'}), 400

    sender_balance, receiver_balance = transfer.sender.balance, transfer.receiver.balance
    sender_balance -= transfer.amount
    receiver_balance += transfer.amount
    receiver_balance %= 2048

    transfer.sender.balance = sender_balance
    transfer.receiver.balance = receiver_balance
    transfer.is_received = True
    app.db.commit()

    return flask.jsonify({'status': 'ok'})


@utils.authenticate_user()
def new_banner(app, partner):
    data = flask.request.json

    try:
        name = data['name']
        assert isinstance(name, str) and name != ''

        banner_format = data['format']
        assert banner_format in ['image', 'video', 'text']

        content = data['content']
        assert isinstance(content, str) and content != ''
    except (AssertionError, KeyError):
        return flask.jsonify({'status': 'error', 'message': 'Malformed API call.'}), 400

    banner = models.Banner(name=name, format=banner_format, content=content, owner_id=partner.id)
    app.db.add(banner)
    app.db.commit()

    return flask.jsonify({'status': 'ok'})



@utils.authenticate_user()
def delete_banner(app, partner, pk):
    try:
        banner = app.db.query(models.Banner).filter(
            models.Banner.id == pk,
            models.Banner.owner_id == partner.id
        ).one()
    except orm.exc.NoResultFound:
        return flask.jsonify({'status': 'error', 'message': 'No banner.'}), 400

    app.db.delete(banner)
    app.db.commit()

    return flask.jsonify({'status': 'ok'})
