from fastapi import FastAPI, status, HTTPException
from scalar_fastapi import get_scalar_api_reference
from typing import Any


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


@app.get("/shipment")
def get_shipment(id: int | None = None) -> dict[str, Any]:
    if not id:
        id = max(shipments.keys())

    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Given id dose not exist."
        )

    return shipments[id]


@app.post("/shipment")
def submit_shipment(data: dict[str, Any]) -> dict[str, Any]:
    content = data["content"]
    weight = data["weight"]
    if weight > 25:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Maximum weight limit is 25",
        )
    new_id = max(shipments.keys()) + 1
    shipments[new_id] = {
        "weight": weight,
        "content": content,
        "status": "placed",
    }

    return {"id": new_id}


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


@app.patch("/shipment")
def patch_shipment(
    id: int,
    content: str | None = None,
    weight: float | None = None,
    status: str | None = None,
):
    shipment = shipments[id]
    # Update the provided fields
    if content:
        shipment["content"] = content
    if weight:
        shipment["weight"] = weight
    if status:
        shipment["status"] = status

    shipments[id] = shipment
    return shipment


@app.patch("/shipment_v2")
def patch_shipment_v2(id: int, body: dict[str, Any]):
    shipment = shipments[id]
    shipment.update(body)
    shipments[id] = shipment
    return shipment


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
