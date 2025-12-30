from django import forms
from home import models
from django.forms import modelformset_factory
from django.contrib.auth.models import User, Group


class UniqueItemsEntry(forms.ModelForm):
    class Meta:
        model = models.UniqueItem
        fields = ['name','buffer']
       
ItemsForm = modelformset_factory(model=models.UniqueItem, form=UniqueItemsEntry, extra=0)


class UserGroupForm(forms.ModelForm):
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=False)

    class Meta:
        model = User
        fields = ["username", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            groups = self.instance.groups.all()
            self.fields["group"].initial = groups.first() if groups.exists() else None

    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            user.save()
            user.groups.clear()
            if self.cleaned_data["group"]:
                user.groups.add(self.cleaned_data["group"])

        return user

UserFormSet = modelformset_factory(model=User, form=UserGroupForm, extra=0) 