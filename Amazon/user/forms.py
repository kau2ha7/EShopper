from django import forms
from django.contrib.auth.models import User

class MyLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

class MyUserRegistrationForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput(),label='Confirm Password')

    class Meta:
        model = User
        fields = ['username','email','first_name','password','password2']

    def clean(self):
        print("CAlled check pass")
        cleaned_data = super(MyUserRegistrationForm, self).clean()
        print('cleaned_data: ', cleaned_data)
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("password2")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )
        
