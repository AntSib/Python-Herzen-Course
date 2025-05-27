from flask import Blueprint, render_template, request, redirect, url_for
from models.crud_model import CRUDModel
from models.currency_rates import CurrencyRates

bp = Blueprint('main', __name__)


@bp.route('/')
def show():
    db = CRUDModel()
    currency_rates = db._read()

    return render_template('form.html', currency_rates=currency_rates)

@bp.route("/fetch", methods=["POST"])
def fetch():
    db = CRUDModel()
    rates_provider = CurrencyRates()

    codes = request.form.get("codes").split()
    del rates_provider.rates
    
    rates_provider.char_codes = codes
    fresh_rates = rates_provider.rates
    
    db._upsert(fresh_rates)

    return redirect(url_for('main.show'))

@bp.route("/delete/<code>", methods=["POST"])
def delete(code):
    db = CRUDModel()
    db._delete(code)

    return redirect(url_for('main.show'))