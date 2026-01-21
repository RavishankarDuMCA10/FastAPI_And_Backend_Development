from enum import Enum
from pydantic import BaseModel, Field
from random import randint


class ShipmentStatus(str, Enum):
    placed = "placed"
    in_transit = "in transit"
    out_for_delivery = "out for delivery"
    delivered = "delivered"


def random_destination():
    return randint(11000, 11999)


class BaseShipment(BaseModel):
    content: str = Field(description="Contents of the shipment", max_length=30)
    weight: float = Field(
        description="Weight of the shipment in kilograms (kgs)", le=25, ge=1
    )
    destination: int | None = Field(
        description="Destination Zipcode. If not provided will be sent off to a random location.",
        default_factory=random_destination,
    )


class ShipmentRead(BaseShipment):
    status: ShipmentStatus


class ShipmentCreate(BaseShipment):
    pass


class ShipmentUpdate(BaseModel):
    status: ShipmentStatus
