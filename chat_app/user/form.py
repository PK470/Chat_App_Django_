from django import forms 
from django.contrib.auth.models import User


class UserRegistrationForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder':'Enter password'}),
        min_length=8,
        label='Password'
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder':'Enter password'}),
        min_length=8,
        label='Password'
    )
    class Meta:
        model = User
        fields = ('email', 'username','first_name','last_name','password')
        widgets = {
            'email': forms.TextInput(attrs={'class':'validate','placeholder':'Enter email'}),
            'username': forms.TextInput(attrs={'class':'validate','placeholder':'Username'}),
            'first_name': forms.TextInput(attrs={'class':'validate','placeholder':'First_name'}),
            'last_name': forms.TextInput(attrs={'class':'validate','placeholder':'Last_name'}),
            'password': forms.TextInput(attrs={'class': 'validate','type': 'password','placeholder':'password'}),
            'confirm_password': forms.TextInput(attrs={'class': 'validate','placeholder':'Confirm_Password'}),
        }
    def clean(Self):
            cleaned_data = super().clean()
            password = cleaned_data.get('password')
            confirm_pass = cleaned_data.get('confirm_password')
            if password != confirm_pass:
                raise forms.ValidationError('Password does not match')
            return cleaned_data
    
class UserLoginForm(forms.Form):
    """Login form"""
    username = forms.CharField(
        label='Email', 
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'validate','id':'email','placeholder':'UserName'})
    )  
    password = forms.CharField(label='Password', 
                               widget=forms.PasswordInput(
                                   attrs={'class': 'validate','id':'password','placeholder':'Password'}))