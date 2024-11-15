# django forms
from django import forms

from sacco.models import Customer


class CustomerForm(forms.ModelForm): # ensure import is strictly django import forms
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'dob', 'weight', 'gender']

