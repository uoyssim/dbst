from django import forms
from .models import Dev

class UpdateDev(forms.ModelForm):
    class Meta:
        model = Dev
        fields = ('id', 'info', 'addr', 'setting',)
