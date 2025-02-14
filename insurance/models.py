from django.db import models
from core.base_models import BaseModel
from core.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.
class InsuranceModel(BaseModel):
    """
    InsuranceModel is an abstract base model that represents the insurance details of a user.

    Attributes:
        title (CharField): The title of the insurance holder (e.g., Mr., Mrs., Dr.).
        first_name (CharField): The first name of the insurance holder.
        last_name (CharField): The last name of the insurance holder.
        email (EmailField): The email address of the insurance holder.
        phone_number (CharField): The phone number of the insurance holder.
        gender (CharField): The gender of the insurance holder.
        date_of_birth (DateField): The date of birth of the insurance holder.
        address (TextField): The address of the insurance holder.
        city (CharField): The city of the insurance holder.
        state (CharField): The state of the insurance holder.
        owner (ForeignKey): A foreign key reference to the User model, representing the owner of the insurance.
        last_payment_made_at (DateTimeField): Datetime of last successful payment via the processor
        
    Meta:
        abstract (bool): Indicates that this model is abstract and should not be used to create any database table.
    """
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
    last_payment_made_at = models.DateTimeField(_('last payment date'), null=True, blank=True)

    class Meta:
        abstract = True
    

class InsuranceProvider(models.Model):
    """
    Model representing an insurance provider.

    Attributes:
        name (str): The name of the insurance provider.
        interface (str): The name mapped to the Travel Provider interface.
        provides_health (bool): Indicates if the provider offers health insurance.
        provides_auto (bool): Indicates if the provider offers auto insurance.
        provides_travel (bool): Indicates if the provider offers travel insurance.
        is_active (bool): Indicates if the provider is active and can be used
    """
    name = models.CharField(_("name"), max_length=255, null=False, blank=False)
    interface = models.CharField(_("interface"), max_length=255, null=False, blank=False)
    provides_health = models.BooleanField(_("provides health insurance"), default=False)
    provides_auto = models.BooleanField(_("provides auto insurance"), default=False)
    provides_travel = models.BooleanField(_("provides travel insurance"), default=False)
    is_active = models.BooleanField(_("is active"), default=True)

    def __str__(self):
        return self.name

class PolicyPurchaseLog(models.Model):
    """
    Model to log the results of policy purchases and renewals.

    Attributes:
        user (ForeignKey): Reference to the user who made the purchase or renewal.
        insurance_provider (ForeignKey): Reference to the insurance provider.
        content_type (ForeignKey): Reference to the content type of the policy.
        object_id (PositiveIntegerField): ID of the policy object.
        policy (GenericForeignKey): Generic foreign key to the policy.
        action (CharField): The action performed (purchase or renewal).
        status (CharField): The status of the action (success or failure).
        response (TextField): Response from the insurance provider.
        timestamp (DateTimeField): The timestamp when the action was performed.
    """
    class Action(models.TextChoices):
        PURCHASE = 'purchase', _('Purchase')
        RENEWAL = 'renewal', _('Renewal')

    class Status(models.TextChoices):
        SUCCESS = 'success', _('Success')
        FAILURE = 'failure', _('Failure')

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='policy_logs')
    insurance_provider = models.ForeignKey(InsuranceProvider, on_delete=models.CASCADE, related_name='policy_logs')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    policy = GenericForeignKey('content_type', 'object_id')
    action = models.CharField(_('action'), max_length=20, choices=Action.choices)
    status = models.CharField(_('status'), max_length=20, choices=Status.choices)
    response = models.TextField(_('message'), null=True, blank=True)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.action} - {self.status} - {self.timestamp}"


class PaymentAttemptLog(models.Model):
    """
    Model to log the results of payment attempts.

    Attributes:
        user (ForeignKey): Reference to the user who made the payment attempt.
        insurance_provider (ForeignKey): Reference to the insurance provider.
        content_type (ForeignKey): Reference to the content type of the policy.
        object_id (PositiveIntegerField): ID of the policy object.
        policy (GenericForeignKey): Generic foreign key to the policy.
        action (CharField): The action performed (payment attempt).
        status (CharField): The status of the action (success or failure).
        response (TextField): Response from the payment gateway.
        timestamp (DateTimeField): The timestamp when the action was performed.
    """
    class Action(models.TextChoices):
        PAYMENT_ATTEMPT = 'payment_attempt', _('Payment Attempt')

    class Status(models.TextChoices):
        SUCCESS = 'success', _('Success')
        FAILURE = 'failure', _('Failure')

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_logs')
    insurance_provider = models.ForeignKey(InsuranceProvider, on_delete=models.CASCADE, related_name='payment_logs')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    policy = GenericForeignKey('content_type', 'object_id')
    action = models.CharField(_('action'), max_length=20, choices=Action.choices, default=Action.PAYMENT_ATTEMPT)
    status = models.CharField(_('status'), max_length=20, choices=Status.choices)
    response = models.TextField(_('response'), null=True, blank=True)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.action} - {self.status} - {self.timestamp}"