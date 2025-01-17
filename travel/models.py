from django.db import models
from insurance.models import InsuranceModel
from django.utils.translation import gettext_lazy as _

# Create your models here.
class TravelInsurance(InsuranceModel):
    nok_full_name = models.CharField(_('next of kin (full name)'), max_length=300, null=False, blank=False)
    nok_address = models.TextField(_('next of kin address'), null=False, blank=False)
    nok_relationship = models.CharField(_('next of kin relationship'), max_length=100, null=False, blank=False)