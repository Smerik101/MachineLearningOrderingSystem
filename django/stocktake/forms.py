from django import forms
from . import models
from django.forms import modelformset_factory


class StocktakeEntry(forms.ModelForm):
    class Meta:
        model = models.StocktakeItem
        fields = ['name','counted']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].disabled = True
       
     
StocktakeItemsFormSet = modelformset_factory(models.StocktakeItem, form=StocktakeEntry, extra=0)
    
