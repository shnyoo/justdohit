from django import forms
from .models import Ride, Travel

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

        # 여행 시작
        self.fields['start_date'].widget.attrs = {
            'id': 'start_date',
            'placeholder': 'Enter Start Date'
        }

        # 차량 반납 날
        self.fields['arriv_date'].widget.attrs = {
            'id': 'arrive_date',
            'placeholder': 'Enter Arrival Date'
        }

        self.fields['travelerNum'].widget.attrs = {
            'id': 'travelerNum',
            'placeholder': 'Enter the number of passengers'
        }

class RideForm(forms.ModelForm):
    class Meta:
        model = Ride
        fields = ['dest', 'arriv_time']
