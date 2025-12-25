from app.models.crud import DBManager
from app.services.currency_rates import CurrencyRates
from flask import Blueprint, render_template, request

bp = Blueprint("main", __name__)


@bp.route("/")
def show():
    """Render the form template."""
    return render_template("form.html")


@bp.route("/fetch", methods=["POST"])
def fetch():
    """
    Fetch the current currency rates from the Central Bank of Russia and update the database.

    Args:
        codes (list): A list of currency codes to fetch

    Returns:
        dict: A dictionary containing the fetched rates

    """
    codes = request.form.get("codes").upper().split()

    provider = CurrencyRates(codes)
    new_rates = provider.fetch()

    db = DBManager()
    db.upsert(new_rates)

    return {
        "rates": new_rates,
    }
