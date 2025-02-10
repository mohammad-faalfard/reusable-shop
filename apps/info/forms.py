from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import ContactUs
from .queries import get_inquiry_categories


class ContactUsForm(forms.ModelForm):
    """
    Form for submitting an inquiry via the 'Contact Us' page.
    Includes fields for name, email, subject, message, relevant URL, and category.
    """

    # Optional custom clean method for additional validation if needed
    def clean_message(self):
        """
        Custom validation for the message field.
        Ensures that the message is not empty or too short.
        """
        message = self.cleaned_data.get("message")
        if not message or len(message) < 10:
            raise ValidationError(_("Message must be at least 10 characters long."))
        return message

    class Meta:
        model = ContactUs
        fields = [
            "name",
            "email",
            "subject",
            "category",
            "relevant_url",
            "message",
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control border mb-3",
                    "id": "username",
                    "type": "text",
                    "placeholder": _("Name"),
                    "name": "username",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control border mb-3",
                    "id": "email",
                    "type": "email",
                    "placeholder": _("Email"),
                    "name": "email",
                }
            ),
            "subject": forms.TextInput(
                attrs={
                    "class": "form-control border mb-3",
                    "id": "subject",
                    "type": "text",
                    "placeholder": _("Subject"),
                    "name": "subject",
                }
            ),
            "category": forms.Select(
                attrs={
                    "class": "mb-3 w-100 border",
                    "id": "topicSelect",
                    "name": "topic",
                }
            ),
            "relevant_url": forms.URLInput(
                attrs={
                    "class": "form-control border mb-3",
                    "id": "relevant_url",
                    "type": "url",
                    "placeholder": _("Relevant URL"),
                    "name": "relevant_url",
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "form-control border mb-3",
                    "id": "message",
                    "cols": "30",
                    "rows": "10",
                    "placeholder": _("Text"),
                    "name": "message",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        """
        Customize the form initialization to add dynamic properties or customize widgets.
        """
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = get_inquiry_categories()

    # Optional custom clean methods for specific fields
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if "example.com" in email:  # Just an example validation
            raise ValidationError(_("Email domain 'example.com' is not allowed."))
        return email
