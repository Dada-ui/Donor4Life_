from django.db import models
from django.utils import timezone
from django.urls import reverse
import datetime
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.conf import settings
import secrets
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from app.managers import UserManager
from django.core.validators import RegexValidator
from django.core.validators import MinLengthValidator, MaxLengthValidator


# Create your models here.


#----------------------------------------------------------------- User #

class CustomUser(AbstractUser):
    roles = models.CharField(max_length=12, error_messages={'required': "Role must be provided"})
    
    USERNAME_FIELD = ("")
    REQUIRED_FIELDS = [""]
    
    def _str__(self):
        return self.email
    

#----------------------------------------------------------------- OTP Token #
    
class OtpToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="otps")
    otp_code = models.CharField(max_length=6, default=secrets.token_hex(3))
    tp_created_at = models.DateTimeField(auto_now_add=True)
    otp_expires_at = models.DateTimeField(blank=True, null=True)


#----------------------------------------------------------------- Organ #
    
class Organ(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


#----------------------------------------------------------------- Hospital #
    
class Hospital(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    

#----------------------------------------------------------------- Contact #

class Contact(models.Model):
    email = models.EmailField()
    subject = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
     
    def __str__(self):
        return self.email

#----------------------------------------------------------------- Profile #

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    email = models.EmailField(max_length=254)
    username = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.username
    

#----------------------------------------------------------------- Donor #

GENDER_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female'),
    ('transgender', 'Transgender'))

BLOOD_GROUP = (
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('O+', 'O+'),
    ('O-', 'O-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'))

ORGAN_CHOICES = (
    ('Brain', 'Brain'),
    ('Lungs', 'Lungs'),
    ('Kidneys', 'Kidneys'),
    ('Heart', 'Heart'),
    ('Birth Tissue', 'Birth Tissue'),
    ('Large Intestines', 'Large Intestines'),
    ('Small Intestines', 'Small Intestines'),
    ('Spinal Cord', 'Spinal Cord'),
    ('Eyes', 'Eyes'),
    ('Pancreas', 'Pancreas'),
    ('Cornea', 'Cornea'),
    ('Tissues', 'Tissues'))
    
class Donor(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    organ = models.CharField(choices=GENDER_CHOICES, max_length=200, blank=True, null=True)
    hospital = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    profile_photo = models.ImageField(upload_to='Profile_photo/', blank=True, null=True)
    full_name = models.CharField(max_length=200, blank=True, null=True)
    dob = models.DateField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES, blank=True, null=True)
    blood_group = models.CharField(max_length=50, choices=BLOOD_GROUP, blank=True, null=True)
    full_address = models.CharField(max_length=500, blank=True, null=True)
    adhaar = models.IntegerField(max_length=12,validators=[RegexValidator(regex = ("^[0-9]{4}\\" + "s[0-9]{4}\\s[0-9]{4}$"), message='Aadhaar number must be exactly 12 digits.')])
    phone_number = models.IntegerField(max_length=10,validators=[RegexValidator(regex = ("^[0-9]{4}\\" + "s[0-9]{3}\\s[0-9]{3}$"), message='Phone number must be exactly 10 digits.')])
    health_card = models.FileField(upload_to='Health_card/', blank=True, null=True, max_length=100)
    family_mail = models.EmailField(max_length=254)
    family_phone_number = models.IntegerField(max_length=10,validators=[RegexValidator(regex = ("^[0-9]{4}\\" + "s[0-9]{3}\\s[0-9]{3}$"), message='Phone number must be exactly 10 digits.')])
    family_address = models.CharField(max_length=500, blank=True, null=True)
    donating_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    def creat(self):
        return self.created_at.strftime('%B %d %Y')

    @property
    def is_now(self):
        return self.donating_date <= timezone.now()

#----------------------------------------------------------------- Recipient Slot Booking #
    
class Recipient_Booking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    organ = models.CharField(max_length=200, blank=True, null=True)
    hospital = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    full_name = models.CharField(max_length=200, blank=True, null=True)
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES, blank=True, null=True)
    blood_group = models.CharField(max_length=50, choices=BLOOD_GROUP, blank=True, null=True)
    full_address = models.CharField(max_length=500, blank=True, null=True)
    adhaar = models.IntegerField(max_length=12,validators=[RegexValidator(regex = ("^[0-9]{4}\\" + "s[0-9]{4}\\s[0-9]{4}$"), message='Aadhaar number must be exactly 12 digits.')])
    phone_number = models.IntegerField(max_length=10,validators=[RegexValidator(regex = ("^[0-9]{4}\\" + "s[0-9]{3}\\s[0-9]{3}$"), message='Phone number must be exactly 10 digits.')])
    receiving_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    created_at = models.DateTimeField(default=timezone.now)

    def clean_datetime_field(self):
        datetime = self.cleaned_data['receiving_date']
        if datetime < timezone.now():
            raise forms.ValidationError("Datetime cannot be in the past")
        return datetime


#----------------------------------------------------------------- Camping #
    
class DonationCamp(models.Model):
    hospital_name = models.CharField(max_length=100)
    hospital_location = models.CharField(max_length=100)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    duration = models.IntegerField()

    def __str__(self):
        return f"{self.hospital_name} on {self.date}"