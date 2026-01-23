from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from typing import Any

from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference

from .database.models import Shipment, ShipmentStatus
from .database.session import SessionDep, create_db_tables
from .schemas import ShipmentCreate, ShipmentRead, ShipmentUpdate


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    print("Server started...")
    create_db_tables()
    yield
    print("...stopped!")


app = FastAPI(lifespan=lifespan_handler)


### Read a shipment by id
@app.get("/shipment", response_model=ShipmentRead)
def get_shipment(id: int, session: SessionDep):
    # Check for shipment with given id
    shipment = session.get(Shipment, id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Given id dose not exist!"
        )

    return shipment


### Create a new shipment with content and weight
@app.post("/shipment")
def submit_shipment(shipment: ShipmentCreate, session: SessionDep) -> dict[str, Any]:
    # Create and assign shipment a new id
    new_shipment = Shipment(
        **shipment.model_dump(),
        status=ShipmentStatus.placed,
        estimated_delivery=datetime.now() + timedelta(days=3),
    )
    session.add(new_shipment)
    session.commit()
    session.refresh(new_shipment)
    # Return id for later use
    return {"id": new_shipment.id}


### Update field of a shipment
@app.patch("/shipment", response_model=ShipmentRead)
def update_shipment(id: int, shipment_update: ShipmentUpdate, session: SessionDep):
    # Update data with given fields
    update = shipment_update.model_dump(exclude_none=True)

    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data provided to update",
        )
    shipment = session.get(Shipment, id)

    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Shipment with id {id} not found",
        )

    shipment.sqlmodel_update(update)

    session.add(shipment)
    session.commit()
    session.refresh(shipment)

    return shipment


### Delete a shipment by id
@app.delete("/shipment")
def delete_shipment(id: int, session: SessionDep) -> dict[str, Any]:
    # Remove from datastore
    session.delete(session.get(Shipment, id))
    session.commit()
    return {"detail": f"Shipment with id {id} is deleted!"}


@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )
