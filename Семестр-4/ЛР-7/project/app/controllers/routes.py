from flask import Blueprint, render_template, request, redirect, url_for
from app.models.crud_model import CRUDModel
from app.services.currency_rates import CurrencyRates

bp = Blueprint('main', __name__)


@bp.route('/')
def show():
    db = CRUDModel()
    currency_rates = db._read_all()

    return render_template('form.html', currency_rates=currency_rates)

@bp.route("/fetch", methods=["POST"])
def fetch():
    codes = request.form.get("codes").split()
    
    rates_provider = CurrencyRates()
    del rates_provider.rates
    rates_provider.char_codes = codes
    new_rates = rates_provider.rates

    db = CRUDModel()
    db._upsert(new_rates)

    return redirect(url_for('main.show'))

@bp.route("/delete/<currency_code>", methods=["POST"])
def delete(currency_code):
    db = CRUDModel()
    db._delete(currency_code)

    return redirect(url_for('main.show'))