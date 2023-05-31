from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget



PAYMENT = (
    ('S','Swahilies'),
    ('C','cash on Delivery')
)

class checkoutForm(forms.Form):
    address = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label="Adress")
    second_address = forms.CharField(
        widget=forms.TextInput(attrs={'class':'form-control'}), required=False, label="Second Address")
    country = forms.CharField(max_length=100)
    zip_code = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label="Phone")
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}), label="Email")
    payment = forms.ChoiceField(widget=forms.RadioSelect(), choices=PAYMENT)

