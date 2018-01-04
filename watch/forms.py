from django import forms
from django.forms.models import ModelForm

from .models import Watch

class WatchForm(ModelForm):
    class Meta:
        model = Watch
        fields = ['url']
