from fastapi import FastAPI, status, HTTPException
from scalar_fastapi import get_scalar_api_reference
from typing import Any
from contextlib import asynccontextmanager
from .database import Database
from .database.session import create_db_tables
from .schemas import (
    ShipmentCreate,
    ShipmentRead,
    ShipmentUpdate,
)


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    print("Server started...")
    create_db_tables()
    yield
    print("...stopped!")


app = FastAPI(lifespan=lifespan_handler)

db = Database()


### Read a shipment by id
@app.get("/shipment", response_model=ShipmentRead)
def get_shipment(id: int):
    # Check for shipment with given id
    shipment = db.get(id)
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Given id dose not exist!"
        )

    return shipment


### Create a new shipment with content and weight
@app.post("/shipment")
def submit_shipment(shipment: ShipmentCreate) -> dict[str, Any]:
    # Create and assign shipment a new id
    new_id = db.create(shipment)
    # Return id for later use
    return {"id": new_id}


### Update field of a shipment
@app.patch("/shipment", response_model=ShipmentRead)
def update_shipment(id: int, shipment: ShipmentUpdate):
    # Update data with given fields
    updated_shipment = db.update(id, shipment)
    if updated_shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Given id dose not exist!"
        )
    return updated_shipment


### Delete a shipment by id
@app.delete("/shipment")
def delete_shipment(id: int) -> dict[str, Any]:
    # Remove from datastore
    db.delete(id)
    return {"detail": f"Shipment with id {id} is deleted!"}


@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )
