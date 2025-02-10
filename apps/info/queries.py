from typing import List

from .models import AboutUs, FAQGroup, InquiryCategory, PrivacyPolicy, ShopLocation


def get_about_us_data() -> str:
    """Returns the text of the first About Us entry or an empty string if none exists."""
    about_us_entry = AboutUs.objects.first()
    return about_us_entry.text if about_us_entry else ""


def get_faq_groups() -> List[FAQGroup]:
    """Returns all FAQ groups ordered by priority."""
    return FAQGroup.objects.all().prefetch_related("faqs").order_by("priority")


def get_privacy_policy() -> str:
    """Returns the text of the first Privacy Policy or an empty string if none exists."""
    policy = PrivacyPolicy.objects.first()
    return policy.text if policy else ""


def get_shop_location() -> ShopLocation | None:
    """Return shop location."""
    return ShopLocation.objects.first()


def get_inquiry_categories() -> List[InquiryCategory]:
    """
    Retrieves all inquiry categories, ordered by priority.
    """
    return InquiryCategory.objects.all().order_by("-priority")
