from django import forms

from ..models import Address, User


class EditProfileForm(forms.ModelForm):
    """
    Form for editing user profile details.
    """

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "phone_number", "email"]  # Added first_name and last_name
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }


class EditAddressForm(forms.ModelForm):
    """
    Form for editing user address details.
    """

    class Meta:
        model = Address
        fields = ["title", "postal_code", "city", "street"]

        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control"},
            ),
            "postal_code": forms.TextInput(
                attrs={"class": "form-control"},
            ),
            "city": forms.Select(
                attrs={"class": "form-control"},
            ),
            "street": forms.TextInput(
                attrs={"class": "form-control"},
            ),
        }
