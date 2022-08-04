from django import forms
from django.contrib.auth.forms import UserCreationForm

from marketplace.models import Trader


class TraderCreationForm(UserCreationForm):

    class Meta:
        model = Trader
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name', 'city',)


class TraderSearchForm(forms.Form):
    nickname = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by username..."})
    )


class PublicationSearchForm(forms.Form):
    model = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name..."})
    )


class ProductSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name..."})
    )

    author = forms.ModelChoiceField(
        Trader.objects.all(),
        required=False,
        label="",
        empty_label='Any author'
    )


class ProductForm(forms.Form):
    name = forms.CharField(max_length=255)
    image = forms.ImageField(required=False)
    description = forms.CharField(widget=forms.Textarea)
    price = forms.DecimalField(max_digits=10, decimal_places=2)


class PublicationForm(forms.Form):
    title = forms.CharField(max_length=255)
    text = forms.CharField(widget=forms.Textarea)
