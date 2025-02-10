from django import forms
from django.utils.translation import gettext_lazy as _
from unfold.widgets import UnfoldAdminSelectWidget

from apps.messaging.models import Group


class AddToGroupForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    group = forms.ModelChoiceField(Group.objects, widget=UnfoldAdminSelectWidget, label=_("group"))
