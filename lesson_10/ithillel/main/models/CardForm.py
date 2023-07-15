from django import forms
from .Card import CardModel

class CardForm(forms.ModelForm):
    class Meta:
        model = CardModel
        fields = ['PAN', 'expiration_date', 'CVV', 'issue_date', 'owner_id']
        widgets = {
            'issue_date': forms.DateInput(attrs={'type': 'date'})
        }