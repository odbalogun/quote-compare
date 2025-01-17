from django.db import models
from core.base_models import BaseModel
from core.models import User
from django.utils.translation import gettext_lazy as _

# Create your models here.
class InsuranceModel(BaseModel):
    title = models.CharField(_("title"), max_length=100, null=False, blank=False)
    first_name = models.CharField(_("first name"), max_length=150, null=False, blank=False)
    last_name = models.CharField(_("last name"), max_length=150, null=False, blank=False)
    email = models.EmailField(_('email address'), null=False, blank=False)
    phone_number = models.CharField(_('phone number'), max_length=30, null=False, blank=False)
    gender = models.CharField(_('gender'), max_length=20, null=False, blank=False)
    date_of_birth = models.DateField(_('date of birth'), null=False, blank=False)
    address = models.TextField(_('address'), null=False, blank=False)
    city = models.CharField(_('city'), max_length=150, null=False, blank=False)
    state = models.CharField(_('state'), max_length=150, null=False, blank=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True
    

class InsuranceProvider(models.Model):
    name = models.CharField(_("name"), max_length=255, null=False, blank=False)
    interface = models.CharField(_("interface"), max_length=255, null=False, blank=False)
    provides_health = models.BooleanField(_("provides health insurance"), default=False)
    provides_auto = models.BooleanField(_("provides auto insurance"), default=False)
    provides_travel = models.BooleanField(_("provides travel insurance"), default=False)

    def __str__(self):
        return self.name