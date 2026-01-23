from datetime import datetime
from random import randint

from pydantic import BaseModel, Field

from .database.models import ShipmentStatus


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
    estimated_delivery: datetime


class ShipmentCreate(BaseShipment):
    pass


class ShipmentUpdate(BaseModel):
    status: ShipmentStatus | None = Field(default=None)
    estimated_delivery: datetime | None = Field(default=None)
