from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
user = get_user_model()

class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=150)
    class Meta():
        model = user
        fields = ['name','email','password1','password2']



class MyInfoForm(forms.ModelForm):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={
        'type':'date'
    }))
    class Meta():
        model = user
        fields = ['name', 'en_name', 'personal_email','birth_date','mobile','landline','national_id','avatar','gender','emergency_contact']



class ChangePasswordForm(forms.ModelForm):
    old_password = forms.CharField(min_length=8)
    new_password = forms.CharField(widget=forms.PasswordInput(), min_length=8, max_length=18)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), min_length=8, max_length=18)
    class Meta():
        model = user
        fields = ['old_password','new_password','confirm_password']
