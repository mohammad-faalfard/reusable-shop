from django import forms
from django.forms import ModelForm

from .models import Product, ProductReview


class ProductAdminForm(ModelForm):
    """
    Custom form for the Product model to exclude the current product
    from being selected as its own variant in the Django admin panel.
    """

    class Meta:
        model = Product
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(ProductAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            # Exclude the current product from the variants list
            self.fields["variants"].queryset = self.fields["variants"].queryset.exclude(id=self.instance.id)


class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ["rating", "text"]
        widgets = {
            "rating": forms.RadioSelect(),
            "text": forms.Textarea(attrs={"placeholder": "Write your review...", "rows": 5, "cols": 30}),
        }
