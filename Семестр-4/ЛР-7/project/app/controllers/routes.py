from flask import Blueprint, render_template, request, redirect, url_for
from project.app.models.crud_model import CRUDModel
from project.app.services.currency_rates import CurrencyRates

bp = Blueprint('main', __name__)


@bp.route('/')
def show():
    """
    Render the form.html template with all currency rates.

    Retrieves all currency rates from the database and passes them to the
    'form.html' template for rendering.
    """

    db = CRUDModel()
    currency_rates = db._read_all()

    return render_template('form.html', currency_rates=currency_rates)

@bp.route("/fetch", methods=["POST"])
def fetch():
    """
    Fetch the current currency rates from the Central Bank of Russia and save them to the database.

    Retrieves the currency char codes from the POST request, fetches the current currency rates for the
    specified "char_codes" from the Central Bank of Russia and saves them to the database. Redirects to the
    '/' endpoint after successful insertion.
    """
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
    """
    Delete the specified currency rate from the database.

    Retrieves the specified currency rate from the database based on the "currency_code"
    parameter and deletes it. Redirects to the '/' endpoint after successful deletion.
    """
    db = CRUDModel()
    db._delete(currency_code)

    return redirect(url_for('main.show'))