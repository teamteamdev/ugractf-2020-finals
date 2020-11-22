#!/usr/bin/env python3

import os
import subprocess
from filelock import FileLock
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField, DateField, DecimalField
from wtforms.validators import DataRequired


class AddRetireeForm(FlaskForm):
    first_name = StringField("Первое имя", validators=[DataRequired()])
    last_name = StringField("Последнее имя", validators=[DataRequired()])
    passcode = PasswordField("Секретный числовой код", validators=[DataRequired()])
    date_of_birth = DateField("Дата рождения", validators=[DataRequired()])
    accept_tos = BooleanField("Я соглашаюсь с политикой конфиденциальности и пользовательским соглашением", validators=[DataRequired()])


class AddPaycheckForm(FlaskForm):
    retiree_id = IntegerField("Персональный идентификатор пенсионера", validators=[DataRequired()])
    passcode = PasswordField("Секретный числовой код", validators=[DataRequired()])
    date = DateField("Дата ваучера", validators=[DataRequired()])
    amount = DecimalField("Количество ваучера, ₽", validators=[DataRequired()])
    signature = StringField("Ваша подпись", validators=[DataRequired()])


class ShowPaychecksForm(FlaskForm):
    retiree_id = IntegerField("Персональный идентификатор пенсионера", validators=[DataRequired()])
    passcode = PasswordField("Секретный числовой код", validators=[DataRequired()])


class ChangePasscodeForm(FlaskForm):
    retiree_id = IntegerField("Персональный идентификатор пенсионера", validators=[DataRequired()])
    passcode = PasswordField("Секретный числовой код", validators=[DataRequired()])
    new_passcode = PasswordField("Новый числовой код", validators=[DataRequired()])


app = Flask(__name__)
app.config["SECRET_KEY"] = "seriousbusiness"
data_dir = "data"


def run_query(name, populate):
    with FileLock(os.path.join(data_dir, ".lock")):
        with open(os.path.join(data_dir, "INPUT.TXT"), "w") as f:
            populate(f)
        try:
            os.remove(os.path.join(data_dir, "OUTPUT.TXT"))
        except OSError:
            pass
        subprocess.run([os.path.join("..", name)], cwd=data_dir)
        try:
            with open(os.path.join(data_dir, "OUTPUT.TXT")) as f:
                report = f.read()
        except OSError:
            report = ""
    if len(report) == 0:
        return render_index(error_msg="НЕПРАВИЛЬНЫЙ ЗАПРОС")
    return render_template("report.html", report=report)


def render_index(add_retiree_form=None, add_paycheck_form=None, show_paychecks_form=None, change_passcode_form=None, error_msg=""):
    if add_retiree_form is None:
        add_retiree_form = AddRetireeForm()
    if add_paycheck_form is None:
        add_paycheck_form = AddPaycheckForm()
    if show_paychecks_form is None:
        show_paychecks_form = ShowPaychecksForm()
    if change_passcode_form is None:
        change_passcode_form = ChangePasscodeForm()
    return render_template("index.html",
                           error_msg=error_msg,
                           add_retiree_form=add_retiree_form,
                           add_paycheck_form=add_paycheck_form,
                           show_paychecks_form=show_paychecks_form,
                           change_passcode_form=change_passcode_form)


@app.route('/')
def get_root():
    return render_template("index.html")


@app.route("/add-retiree", methods=["POST", "GET"])
def add_retiree():
    form = AddRetireeForm()
    if form.validate_on_submit():
        def populate(f):
            f.write("{passcode:016d} {last_name:20} {first_name:20} {date_of_birth}".format(
                passcode=int(form.passcode.data),
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                date_of_birth=form.date_of_birth.data.strftime("%Y%m%d"),
            ))
        return run_query("ADD-RETIREE", populate)
    return render_template("add-retiree.html", form=form)


@app.route("/add-paycheck", methods=["POST", "GET"])
def add_paycheck():
    form = AddPaycheckForm()
    if form.validate_on_submit():
        def populate(f):
            f.write("{retiree_id:010d} {passcode:016d} {date} {amount:09.2f} {signature:32}".format(
                retiree_id=form.retiree_id.data,
                passcode=int(form.passcode.data),
                date=form.date.data.strftime("%Y%m%d"),
                amount=form.amount.data,
                signature=form.signature.data,
            ))
        return run_query("ADD-PAYCHECK", populate)
    return render_template("add-paycheck.html", form=form)


@app.route("/show-paychecks", methods=["POST", "GET"])
def show_paychecks():
    form = ShowPaychecksForm()
    if form.validate_on_submit():
        def populate(f):
            f.write("{retiree_id:010d} {passcode:016d}".format(
                retiree_id=form.retiree_id.data,
                passcode=int(form.passcode.data),
            ))
        return run_query("SHOW-PAYCHECKS", populate)
    return render_template("show-paychecks.html", form=form)


@app.route("/change-passcode", methods=["POST", "GET"])
def change_passcode():
    form = ChangePasscodeForm()
    if form.validate_on_submit():
        def populate(f):
            f.write("{retiree_id:010d} {passcode:016d} {new_passcode:016d}".format(
                retiree_id=form.retiree_id.data,
                passcode=int(form.passcode.data),
                new_passcode=int(form.new_passcode.data),
            ))
        return run_query("CHANGE-PASSCODE", populate)
    return render_template("change-passcode.html", form=form)


@app.route("/resolution")
def show_resolution():
    return render_template("show-resolution.html")


if __name__ == "__main__":
    app.run(debug=True)
