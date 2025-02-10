from django import forms
from django.utils.translation import gettext_lazy as _

from .models import PostComment


# Django Form for Comments
class CommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "id": "comments",
                    "cols": "30",
                    "rows": "10",
                    "placeholder": _("Write your comment..."),
                }
            ),
        }
        labels = {
            "text": "",  # No label, as placeholder is used.
        }
