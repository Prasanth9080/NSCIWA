# from django import forms
# from .models import User

# class SignupForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'phone_number', 'password']


# forms.py
from django import forms
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class CustomPasswordResetForm(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise ValidationError("Email is not valid, please enter a valid email.")
        return email


# Bond hold date field
from django import forms
from .models import BondImage

class BondImageForm(forms.ModelForm):
    investment_date = forms.DateField(
        input_formats=['%d.%m.%Y', '%d-%m-%Y', '%d/%m/%Y', '%Y-%m-%d'],
        widget=forms.DateInput(format='%d-%m-%Y', attrs={'placeholder': 'dd-mm-yyyy'})
    )
    dateofresale = forms.DateField(
        input_formats=['%d.%m.%Y', '%d-%m-%Y', '%d/%m/%Y', '%Y-%m-%d'],
        widget=forms.DateInput(format='%d-%m-%Y', attrs={'placeholder': 'dd-mm-yyyy'})
    )

    class Meta:
        model = BondImage
        fields = '__all__'


