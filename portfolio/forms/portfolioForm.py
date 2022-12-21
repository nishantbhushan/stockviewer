from django import forms

from ..models import portfolioModel

class portfolioForm(forms.ModelForm):
    
    class Meta:
        model = portfolioModel
        fields = "__all__"
        # widgets = {
        #     'datePurchased' : forms.DateInput(format='%Y-%m-%d'),
        #     'quantity': forms.NumberInput(),
        #     'costBasis': forms.NumberInput(),
        # } 
    