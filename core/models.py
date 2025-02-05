from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .manager import UserManager
from .base_models import StickyDeleteModel, BaseModel

class User(StickyDeleteModel, AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    middle_name = models.CharField(_("middle name"), max_length=150, null=True, blank=True)
    date_of_birth = models.DateField(_("date of birth"), null=True, blank=True)
    nationality = models.CharField(_("nationality"), max_length=150, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self) -> str:
        return self.email
    

class PasswordResetRequest(BaseModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    token = models.CharField(_('token'), max_length=150)
    expires_at = models.DateTimeField(_('expires at'))


class Country(BaseModel):
    name = models.CharField(_('name'), max_length=100, unique=True, null=False, blank=False)
    code = models.CharField(_('code'), max_length=3, unique=False, null=True, blank=False)
    nationality = models.CharField(_('nationality'), max_length=100, unique=False, null=True, blank=False)

    def __str__(self):
        return self.name
