# from django.db import models
# from django.utils.translation import gettext_lazy as _


# class CouponType(models.IntegerChoices):
#     PERCENT = 0, _("Percent")
#     AMOUNT = 1, _("Amount")


# class DiscountType(models.IntegerChoices):
#     PERCENT = 0, _("Percent")
#     AMOUNT = 1, _("Amount")


# class RatingChoices(models.IntegerChoices):
#     POOR = 1, _("Poor")
#     AVERAGE = 2, _("Average")
#     GOOD = 3, _("Good")
#     VERY_GOOD = 4, _("Very Good")
#     EXCELLENT = 5, _("Excellent")


# class HolderChoices(models.IntegerChoices):
#     MAIN_PAGE_FIRST = 0, _("Main Page - First")
#     MAIN_PAGE_SECOND = 1, _("Main Page - Second")


# class ServiceTypeChoices(models.IntegerChoices):
#     MANUAL = 0, _("Manual")


# class OrderStatusChoices(models.IntegerChoices):
#     PAYMENT_WAITING = 0, _("Payment waiting")
#     ORDER_PLACED = 1, _("Order placed")
#     PRODUCT_PACKAGING = 2, _("Product packaging")
#     READY_FOR_SHIPMENT = 3, _("Ready for shipment")
#     ON_THE_WAY = 4, _("On the way")
#     DROPPED_IN_DELIVERY = 5, _("Dropped in the delivery station")
#     DELIVERED = 6, _("Delivered")
#     CANCELED = 7, _("Canceled")
