from decimal import Decimal


def calculate_service_fee(total_amount: Decimal):
    """
    Calculate the service fee based on the total amount.

    Args:
        total_amount (Decimal): Total amount of the insurance.

    Returns:
        Decimal: Service fee amount.
    """
    return min(total_amount * Decimal('0.1'), 2000)