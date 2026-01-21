from fastapi import FastAPI, status, HTTPException
from scalar_fastapi import get_scalar_api_reference
from typing import Any
from .schemas import Shipment

app = FastAPI()

shipments = {
    12734: {"weight": 0.6, "content": "wooden table", "status": "in transit"},
    12735: {"weight": 2.3, "content": "office chair", "status": "delivered"},
    12736: {"weight": 1.5, "content": "desk lamp", "status": "pending"},
    12737: {"weight": 0.8, "content": "keyboard", "status": "in transit"},
    12738: {"weight": 5.2, "content": "monitor", "status": "in transit"},
    12739: {"weight": 0.4, "content": "mouse", "status": "delivered"},
    12740: {"weight": 3.1, "content": "bookshelf", "status": "pending"},
}


### Read a shipment by id
@app.get("/shipment")
def get_shipment(id: int) -> dict[str, Any]:
    # Check for shipment with given id
    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Given id dose not exist!"
        )

    return shipments[id]


### Create a new shipment with content and weight
@app.post("/shipment")
def submit_shipment(shipment: Shipment) -> dict[str, Any]:
    # Create and assign shipment a new id
    new_id = max(shipments.keys()) + 1
    # Add to shipments dict
    shipments[new_id] = {
        "weight": shipment.weight,
        "content": shipment.content,
        "destination": shipment.destination,
        "status": "placed",
    }
    # Return id for later use
    return {"id": new_id}


### Update field of a shipment
@app.get("/shipment/{field}")
def get_shipment_field(field: str, id: int) -> dict[str, Any]:
    return {field: shipments[id][field]}


@app.put("/shipment")
def shipment_update(
    id: int, content: str, weight: float, status: str
) -> dict[str, Any]:
    shipments[id] = {
        "weight": weight,
        "content": content,
        "status": status,
    }
    return shipments[id]


### Update field of a shipment
@app.patch("/shipment")
def patch_shipment(id: int, body: dict[str, Any]):
    # Update data with given fields
    shipments[id].update(body)
    return shipments[id]


@app.delete("/shipment")
def delete_shipment(id: int) -> dict[str, Any]:
    shipments.pop(id)
    return {"detail": f"Shipment with id {id} is deleted!"}


@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )
