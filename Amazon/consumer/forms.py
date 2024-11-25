from django import forms 
from .models import Customer

class CustomerForm(forms.ModelForm):
    
    class Meta:
        model = Customer
        fields = ("name","locality","city","state","zipcode")
        widgets =  {'name':forms.TextInput(attrs={'class':'form-control'}),
                    'locality':forms.TextInput(attrs={'class':'form-control'}),
                    'city':forms.TimeInput(attrs={'class':'form-control'}),
                    'state':forms.Select(attrs={'class':'form-control'}),
                    'zipcode':forms.NumberInput(attrs={'class':'form-control'})

        }

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name','locality','city','state','zipcode']
        widgets = {'name':forms.TextInput(attrs={'class':'form-control'}),
                   'locality':forms.TextInput(attrs={'class':'form-control'}),
                   'city':forms.TextInput(attrs={'class':'form-control'}),
                   'state':forms.Select(attrs={'class':'form-control'}),
                   'zipcode':forms.NumberInput(attrs={'class':'form-control'}),}
    