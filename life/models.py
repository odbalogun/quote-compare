from django.db import models
from insurance.models import InsuranceModel, InsuranceProvider
from django.utils.translation import gettext_lazy as _

# Create your models here.
class LifeInsurance(InsuranceModel):
    nok_full_name = models.CharField(_('next of kin (full name)'), max_length=300, null=False, blank=False)
    nok_address = models.TextField(_('next of kin address'), null=False, blank=False)
    nok_phone_number = models.CharField(_('phone number'), max_length=30, null=False, blank=False)
    nok_relationship = models.CharField(_('next of kin relationship'), max_length=100, null=False, blank=False)
    insured_amount = models.DecimalField(_('premium amount'), max_digits=10, decimal_places=2, null=True, blank=True)
    policy_number = models.CharField(_('policy number'), max_length=100, null=True, blank=True)
    premium_amount = models.DecimalField(_('premium amount'), max_digits=10, decimal_places=2, null=True, blank=True)
    service_fee = models.DecimalField(_('service fee'), max_digits=10, decimal_places=2, null=True, blank=True)
    tax = models.DecimalField(_('value added tax'), max_digits=10, decimal_places=2, null=True, blank=True)
    total_amount = models.DecimalField(_('total amount'), max_digits=10, decimal_places=2, null=True, blank=True)
    insurance_provider = models.ForeignKey(InsuranceProvider, on_delete=models.SET_NULL, null=True, blank=True, related_name='life_insurances')
    date_purchased = models.DateTimeField(_('date purchased'), null=True, blank=True)
    _metadata = models.JSONField(_('meta data'), null=True, blank=True)
    # benefit_details
    # payment_plan

    @property
    def metadata(self):
        return self._metadata
    
    def metadata(self, key, value):
        self._metadata[key] = value