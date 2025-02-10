from typing import List

from .models import ShipmentType


def get_active_shipment_types() -> List[ShipmentType]:
    """
    Returns a queryset of active shipment types.
    """
    return ShipmentType.objects.active().order_by("price")


def get_shipment_by_id(shipment_id: int) -> ShipmentType:
    """
    Returns a shipment type by its ID.
    """
    try:
        return ShipmentType.objects.get(id=shipment_id)
    except ShipmentType.DoesNotExist:
        return None  # or handle the exception as needed
