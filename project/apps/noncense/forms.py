from django import forms


class MobileForm(forms.Form):
    mobile = forms.CharField(max_length=12)


class NonceForm(forms.Form):
    code = forms.CharField(max_length=4)
