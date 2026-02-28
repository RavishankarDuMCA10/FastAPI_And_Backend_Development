from fastapi import APIRouter
from app.api.dependencies import ServiceDep
from app.api.schemas.shipment import ShipmentCreate, ShipmentRead, ShipmentUpdate
from app.database.models import Shipment
from fastapi import HTTPException, status
from typing import Any

from app.services.shipment import ShipmentService  

router = APIRouter()



### Read a shipment by id
@router.get("/shipment", response_model=ShipmentRead)
async def get_shipment(id: int, service: ServiceDep) -> Shipment:
    # Check for shipment with given id
    shipment = await service.get(id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Given id dose not exist!"
        )

    return shipment


### Create a new shipment with content and weight
@router.post("/shipment")
async def submit_shipment(shipment: ShipmentCreate, service: ServiceDep) -> Shipment:
    # Create and assign shipment a new id
    return await service.add(shipment)


### Update field of a shipment
@router.patch("/shipment", response_model=ShipmentRead)
async def update_shipment(id: int, shipment_update: ShipmentUpdate, service: ServiceDep):
    # Update data with given fields
    update = shipment_update.model_dump(exclude_none=True)

    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data provided to update",
        )
    
    shipment = await service.update(id, shipment_update)
    return shipment


### Delete a shipment by id
@router.delete("/shipment")
async def delete_shipment(id: int, service: ServiceDep) -> dict[str, Any]:
    # Remove from datastore
    await service.delete(id)
    return {"detail": f"Shipment with id {id} is deleted!"}