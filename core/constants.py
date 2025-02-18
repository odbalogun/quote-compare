from django.utils.translation import gettext_lazy as _
from django.db import models

VAT_TAX = 7.5
MAX_SERVICE_FEE = 2000.00

class PolicyStatus(models.TextChoices):
    QUOTE = 'quote', _('Quote')
    CONFIRMED = 'confirmed', _('Confirmed')
    PAID = 'paid', _('Paid')
    POLICY_PURCHASED = 'policy purchased', _('Policy Purchased')
    CANCELLED_BEFORE_PURCHASE = 'cancelled before purchase', _('Cancelled Before Purchase')
    CANCELLED_BEFORE_RENEWAL = 'cancelled before renewal', _('Cancelled Before Renewal')
    EXPIRED = 'expired', _('Expired')