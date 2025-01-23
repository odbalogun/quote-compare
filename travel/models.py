from django.db import models
from insurance.models import InsuranceModel
from django.utils.translation import gettext_lazy as _
from core.models import Country

# Create your models here.
class TravelInsurance(InsuranceModel):
    nok_full_name = models.CharField(_('next of kin (full name)'), max_length=300, null=False, blank=False)
    nok_address = models.TextField(_('next of kin address'), null=False, blank=False)
    nok_relationship = models.CharField(_('next of kin relationship'), max_length=100, null=False, blank=False)
    pre_existing_medical_condition = models.BooleanField(_('pre-existing medical condition'), default=False)
    passport_no = models.CharField(_('passport number'), max_length=50, null=False, blank=False)
    start_date = models.DateField(_('start date'), null=False, blank=False)
    end_date = models.DateField(_('end date'), null=False, blank=False)
    passport_image_path = models.CharField(_('passport image path'), max_length=255, null=True, blank=True)
    destination_country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True, related_name='travel_insurances')

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