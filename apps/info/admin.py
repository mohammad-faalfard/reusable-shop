# apps/info/admin.py

# Standard Library Imports
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

# Third-Party Imports
from leaflet.admin import LeafletGeoAdmin

# Local Imports
from core.admin import BaseModelAdmin

from .models import FAQ, AboutUs, City, ContactUs, FAQGroup, InquiryCategory, PrivacyPolicy, ShopLocation, State


# AboutUs Admin Configuration
@admin.register(AboutUs)
class AboutUsAdmin(BaseModelAdmin):
    list_display = ["id", "created_by", "updated_by", "created_at", "updated_at"]
    search_fields = ["text"]
    list_filter = ["created_at"]
    ordering = ["-created_at"]
    fieldsets = ((None, {"fields": ("text",)}),)

    def has_add_permission(self, request):
        """Limit to only one record by checking if a record already exists."""
        return not self.model.objects.exists()


# FAQ Admin Configuration
@admin.register(FAQ)
class FAQAdmin(BaseModelAdmin):
    list_display = ["id", "title", "faq_group", "priority"]
    search_fields = ["title", "answer"]
    list_filter = ["faq_group", "priority"]
    ordering = ["priority"]
    fieldsets = ((None, {"fields": ("priority", "title", "logo", "answer", "faq_group")}),)


# FAQGroup Admin Configuration
@admin.register(FAQGroup)
class FAQGroupAdmin(BaseModelAdmin):
    list_display = ["id", "title", "updated_by", "created_at", "updated_at"]
    search_fields = ["title"]
    fieldsets = ((None, {"fields": ("priority", "title")}),)


# PrivacyPolicy Admin Configuration
@admin.register(PrivacyPolicy)
class PrivacyPolicyAdmin(BaseModelAdmin):
    list_display = ["id", "short_text", "created_by", "updated_by", "created_at", "updated_at"]
    fieldsets = ((None, {"fields": ("text",)}),)

    def short_text(self, obj):
        """Display the first 10 characters of the text field."""
        return obj.text[:10] + "..." if len(obj.text) > 10 else obj.text

    short_text.short_description = _("Text")

    def has_add_permission(self, request):
        """Limit to only one record by checking if a record already exists."""
        return not self.model.objects.exists()


# ShopLocation Admin Configuration
@admin.register(ShopLocation)
class ShopLocationAdmin(LeafletGeoAdmin, BaseModelAdmin):
    list_display = ["id", "address", "created_by", "updated_by", "created_at", "updated_at", "is_active"]
    search_fields = ["address"]
    fieldsets = ((None, {"fields": ("is_active", "address", "location")}),)

    def short_text(self, obj):
        """Display the first 10 characters of the address field."""
        return obj.address[:10] + "..." if len(obj.address) > 10 else obj.address

    short_text.short_description = _("Address")


# City Admin Configuration
@admin.register(City)
class CityAdmin(BaseModelAdmin):
    list_display = ["id", "title", "state", "updated_by", "created_at", "updated_at", "is_active"]
    search_fields = ["title"]
    list_filter = ["state"]
    fieldsets = ((None, {"fields": ("title", "state")}),)


# State Admin Configuration
@admin.register(State)
class StateAdmin(BaseModelAdmin):
    list_display = ["id", "title", "updated_by", "created_at", "updated_at", "priority", "is_active"]
    search_fields = ["title"]
    fieldsets = ((None, {"fields": ("priority", "title")}),)


# Register the ContactUs model
@admin.register(ContactUs)
class ContactUsAdmin(BaseModelAdmin):
    list_display = (
        "id",
        "name",
        "email",
        "category",
        "subject",
        "relevant_url",
        "message",
        "created_at",
    )
    search_fields = ("name", "email", "subject")
    list_filter = ("created_at",)


# Register the InquiryCategory model
@admin.register(InquiryCategory)
class CategoryAdmin(BaseModelAdmin):
    list_display = ("id", "title", "created_at", "priority")
    search_fields = ("title",)
    list_filter = ("created_at",)
