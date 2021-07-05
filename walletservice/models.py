from django.db import models

# Create your models here.

from django.contrib.auth.models import User

TRANSACTIONTYPE = (
    ("deposit", "deposit"),
    ("withdraw", "withdraw"),
)

TRANSACTIONSTATUS = (
    ("success", "success"),
    ("fail", "withdraw"),
)

class AbstractBase(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'AbstractBase'
        abstract = True

class Wallete(AbstractBase):
    owner = models.OneToOneField(User, 
                on_delete=models.CASCADE, 
                related_name="owner_wallete")
    is_active = models.BooleanField(default=True)
    is_enable = models.BooleanField(default=False)
    enabled_at = models.DateTimeField(null=True, blank=True)
    disabled_at = models.DateTimeField(null=True, blank=True)
    balance = models.CharField(max_length=255, null=True, blank=True, default=0)
    
    class Meta:
        db_table = "Wallete"
    

class Transactions(AbstractBase):
    user = models.ForeignKey(User,
                on_delete=models.CASCADE, 
                related_name="user_transaction")
    is_active = models.BooleanField(default=True)
    datetime = models.DateTimeField(auto_now=True)
    reference_id = models.CharField(max_length=100, null=True)
    amount = models.CharField(max_length=255, null=True, blank=True)
    wallet = models.ForeignKey(Wallete, 
            on_delete=models.CASCADE)
    is_success = models.BooleanField(default=False)
    type = models.CharField(max_length=50,
                choices=TRANSACTIONTYPE)

    class Meta:
        db_table = "Transactions"
