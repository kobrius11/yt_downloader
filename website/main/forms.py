from django import forms
from django.utils.translation import gettext_lazy as _

class SearchQuary(forms.Form):
    search_string = forms.CharField(label=_('Insert youtube playlist url'), max_length=150, required=True)
    
