from django import forms
from .models import Vehicle, Travel

class TravelForm(forms.ModelForm):
    class Meta:
        model = Travel
        fields = ['start', 'dest', 'start_date', 'arriv_date', 'travelerNum']

    def __init__(self, *args, **kwargs):
        super(TravelForm, self).__init__(*args, **kwargs)

        self.fields['start'].widget.attrs = {
            'id': 'start-input',
            'placeholder': "Enter your address or zip code"
        }

        self.fields['dest'].widget.attrs = {
            'id': 'dest-input',
            'placeholder': "Enter destination"
        }