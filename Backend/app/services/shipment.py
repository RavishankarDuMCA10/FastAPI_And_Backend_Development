from datetime import datetime, timedelta

from fastapi import HTTPException, status
from app.api.schemas.shipment import ShipmentCreate, ShipmentUpdate
from app.database.models import Shipment, ShipmentStatus
from sqlalchemy.ext.asyncio import AsyncSession


class ShipmentService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: int) -> Shipment:
        # Logic to get a shipment by id
        return await self.session.get(Shipment, id)

    async def add(self, shipment_create: ShipmentCreate) -> Shipment:
        # Logic to add a new shipment
        new_shipment = Shipment(
            **shipment_create.model_dump(),
            status=ShipmentStatus.placed,
            estimated_delivery=datetime.now() + timedelta(days=3),
        )
        self.session.add(new_shipment)
        await self.session.commit()
        await self.session.refresh(new_shipment)
        return new_shipment

    async def update(self, shipment_update: ShipmentUpdate) -> Shipment:
        # Logic to update an existing shipment
        shipment = await self.get(id)

        if not shipment:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Shipment with id {id} not found",
            )
        shipment.sqlmodel_update(shipment_update)

        self.session.add(shipment)
        await self.session.commit()
        await self.session.refresh(shipment)

        return shipment

    async def delete(self, id: int) -> None:
        # Logic to delete a shipment by id
        await self.session.delete(self.get(Shipment, id))
        await self.session.commit()