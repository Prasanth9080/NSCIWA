from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)
    jwt_token = models.CharField(max_length=500, blank=True, null=True)
    is_main_user = models.BooleanField(default=False)  # 🔐 Add this
    is_sub_mainuser = models.BooleanField(default=False)
    parent_user = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.username

### another file models

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class MyKYC(models.Model):
    MEMBERSHIP_CHOICES = [
        ('senior', 'Senior'),
        ('junior', 'Junior')
    ]
    BOND_IMAGE_TYPE_CHOICES = [
        ('original', 'Original'),
        ('xerox', 'Xerox'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_kycs")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_my_kycs")

    membershipno = models.IntegerField(null=True, blank=True)
    membershiptype = models.CharField(max_length=10, choices=MEMBERSHIP_CHOICES, blank=True)
    depositorsname = models.CharField(max_length=100, blank=True)
    depositorsaddress = models.TextField(blank=True)
    nameofthecompany = models.CharField(max_length=100, blank=True)

    customeridno = models.IntegerField(null=True, blank=True)
    receiptno = models.IntegerField(null=True, blank=True)
    modno = models.IntegerField(null=True, blank=True)

    depositamount = models.IntegerField(null=True, blank=True)
    intrefundamount = models.IntegerField(null=True, blank=True)
    defaultamount = models.IntegerField(null=True, blank=True)

    investmentdate = models.DateTimeField(default=timezone.now)

    bondholdername = models.CharField(max_length=100, blank=True)
    projectname = models.CharField(max_length=100, blank=True)
    depositormobile_number = models.CharField(max_length=12, blank=True)

    agentname = models.CharField(max_length=100, blank=True)
    agentaddress = models.TextField(blank=True)

    bondimage = models.ImageField(upload_to='kyc_uploads/', null=True, blank=True)
    bondimagetype = models.CharField(max_length=10, choices=BOND_IMAGE_TYPE_CHOICES, null=True, blank=True)
    nameofdirector = models.CharField(max_length=100, blank=True)
    aadhar_number = models.CharField(max_length=20, blank=True)
    pan_number = models.CharField(max_length=20, blank=True)
    ration_number = models.CharField(max_length=20, blank=True)

    bankname = models.CharField(max_length=100, blank=True)
    bankaccno = models.CharField(max_length=20, blank=True)
    ifscno = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"KYC for {self.depositorsname} - {self.projectname}"



# -----------------------------
# Model 2: SubKYC (Sub KYC)
# -----------------------------
class SubKYC(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sub_kycs", default='')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sub_kycs_created')
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    mobile_number = models.CharField(max_length=15)
    fathername = models.CharField(max_length=100)
    address = models.TextField()
    aadhar_number = models.CharField(max_length=20)
    aadhar_front_image = models.ImageField(upload_to='sub_aadhar_front/', blank=True, null=True)
    aadhar_back_image = models.ImageField(upload_to='sub_aadhar_back/', blank=True, null=True)
    profession = models.CharField(max_length=100)
    contactSH = models.CharField(max_length=100)
    nameSH = models.CharField(max_length=100)
    investmentamt = models.DecimalField(max_digits=12, decimal_places=2)
    passportphoto = models.ImageField(upload_to='sub_passport_photos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_hidden = models.BooleanField(default=False)

    def __str__(self):
        return f"SubKYC: {self.name}"

# -----------------------------
# Common Model: Bond Images
# -----------------------------
from decimal import Decimal
import datetime
from django.db import models

class BondImage(models.Model):
    my_kyc = models.ForeignKey("MyKYC", on_delete=models.CASCADE, null=True, blank=True, related_name='bonds')
    sub_kyc = models.ForeignKey("SubKYC", on_delete=models.CASCADE, null=True, blank=True, related_name='bonds')
    image = models.ImageField(upload_to='bonds/')
    companyname = models.CharField(max_length=100,)
    projectname = models.CharField(max_length=100,)
    investment_date = models.DateField(default=datetime.date.today)  # ✅ CORRECT DEFAULT
    customer_id = models.CharField(max_length=10,)
    amount = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return f"BondImage ({self.image.name})"

# trial

# from django.db import models

# class product(models.Model):
#     name = models.CharField(max_length=30),
#     price = models.IntegerField(max_length=10, decimal_place=2)
#     created_at = models.DateTimeField(auto_created=True)

#     def __str__(self):
#         return self.name

# from django.db import models 

# class product(models.Model):
#     name = models.CharField(max_length=20),
#     price = models.FloatField(max_length=10, decimal_place=2),
#     created_at = models.DateTimeField()
#     file = models.FileField()

#     def __str__(self):
#         return self.name