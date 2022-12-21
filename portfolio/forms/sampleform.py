from django import forms
from ..models import samplemodel

class normalform(forms.Form):
    # textInput= forms.CharField()
    # numberInput = forms.IntegerField()
    # decimalInput =forms.DecimalField()
    # dateInput = forms.DateField()
    # dateInput.widget =forms.DateInput(format='%Y-%m-%d')
    userId =forms.IntegerField()
    ticker = forms.CharField()
    datePurchased = forms.DateField()
    datePurchased.widget =forms.DateInput(format='%Y-%m-%d')
    quantity = forms.DecimalField()
    costBasis = forms.DecimalField()
    buyType = forms.CharField()
    country = forms.CharField()

class normalModelForm(forms.ModelForm):

    class Meta:
        model = samplemodel
        fields = "__all__"
