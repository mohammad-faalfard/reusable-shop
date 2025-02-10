from django.contrib.gis.db import models as gmodels
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel, CreatedByMixin, UpdatedByMixin


class ShopLocation(BaseModel, CreatedByMixin, UpdatedByMixin):
    """
    Represents a shop's physical location with an address and precise geographical coordinates.

    Attributes:
        address (CharField): The address of the shop location, limited to 200 characters.
        location (PointField): The geographical location using latitude and longitude.
    """

    address = gmodels.CharField(
        max_length=200,
        verbose_name=_("Address"),
        help_text=_("The physical address of the shop location."),
    )
    location = gmodels.PointField(
        srid=4326,  # Standard spatial reference system for latitude/longitude
        verbose_name=_("Location"),
        help_text=_("Geographical coordinates (longitude, latitude) of the shop location."),
        null=False,  # Ensuring location is mandatory
        blank=False,
    )

    def clean(self):
        """
        Custom validation to ensure that the latitude and longitude are within valid ranges.
        """
        if self.location:
            # Latitude range: -90 to 90
            if self.location.y < -90 or self.location.y > 90:
                raise ValidationError(_("Latitude must be between -90 and 90 degrees."))
            # Longitude range: -180 to 180
            if self.location.x < -180 or self.location.x > 180:
                raise ValidationError(_("Longitude must be between -180 and 180 degrees."))

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = _("Shop Location")
        verbose_name_plural = _("Shop Locations")
