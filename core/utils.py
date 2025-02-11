from decimal import Decimal
from core.constants import MAX_SERVICE_FEE, VAT_TAX


def calculate_value_added_tax(amount: Decimal):
    return amount * (VAT_TAX / 100)


def calculate_service_fee(amount: Decimal):
    """
    Calculate the service fee based on the total amount.

    Args:
        amount (Decimal): Total amount of the insurance.

    Returns:
        Decimal: Service fee amount.
    """
    return min(amount * Decimal("0.1"), MAX_SERVICE_FEE)
