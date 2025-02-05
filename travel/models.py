from django.db import models
from insurance.models import InsuranceModel, InsuranceProvider
from django.utils.translation import gettext_lazy as _
from core.models import Country

# Create your models here.
class TravelInsurance(InsuranceModel):
    """
    TravelInsurance model to store travel insurance details.

    Attributes:
        nok_full_name (CharField): Next of kin's full name.
        nok_address (TextField): Next of kin's address.
        nok_relationship (CharField): Relationship with the next of kin.
        pre_existing_medical_condition (BooleanField): Indicates if there is a pre-existing medical condition.
        passport_no (CharField): Passport number of the insured.
        start_date (DateField): Start date of the insurance coverage.
        end_date (DateField): End date of the insurance coverage.
        passport_image_path (CharField): Path to the image of the passport.
        destination_country (ForeignKey): Destination country for the travel insurance.
        status (CharField): Status of the insurance (Quote, Purchased, Expired).
        policy_number (CharField): Policy number of the insurance.
        premium_amount (DecimalField): Premium amount of the insurance.
        total_amount (DecimalField): Total amount of the insurance including fees.
        insurance_provider (ForeignKey): Reference to the insurance provider.

    Status:
        QUOTE: Insurance quote.
        PURCHASED: Insurance purchased.
        EXPIRED: Insurance expired.
    """
    nok_full_name = models.CharField(_('next of kin (full name)'), max_length=300, null=False, blank=False)
    nok_address = models.TextField(_('next of kin address'), null=False, blank=False)
    nok_relationship = models.CharField(_('next of kin relationship'), max_length=100, null=False, blank=False)
    pre_existing_medical_condition = models.BooleanField(_('pre-existing medical condition'), default=False)
    passport_no = models.CharField(_('passport number'), max_length=50, null=False, blank=False)
    start_date = models.DateField(_('start date'), null=False, blank=False)
    end_date = models.DateField(_('end date'), null=False, blank=False)
    passport_image_path = models.CharField(_('passport image path'), max_length=255, null=True, blank=True)
    destination_country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True, related_name='travel_insurances')
    policy_number = models.CharField(_('policy number'), max_length=100, null=True, blank=True)
    premium_amount = models.DecimalField(_('premium amount'), max_digits=10, decimal_places=2, null=True, blank=True)
    total_amount = models.DecimalField(_('total amount'), max_digits=10, decimal_places=2, null=True, blank=True)
    insurance_provider = models.ForeignKey(InsuranceProvider, on_delete=models.SET_NULL, null=True, blank=True, related_name='travel_insurances')

    class Status(models.TextChoices):
        QUOTE = 'quote', _('Quote')
        PURCHASED = 'purchased', _('Purchased')
        EXPIRED = 'expired', _('Expired')

    status = models.CharField(
        _('status'),
        max_length=20,
        choices=Status.choices,
        default=Status.QUOTE,
    )