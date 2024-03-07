from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from database import Database

app = FastAPI()
db = Database()

class Address(BaseModel):
    latitude: float
    longitude: float
    address: str

@app.post("/addresses/", response_model=Address)
def create_address(address: Address):
    return db.create_address(address)

@app.get("/addresses/", response_model=List[Address])
def get_addresses():
    return db.get_addresses()

@app.delete("/addresses/{address_id}/")
def delete_address(address_id: int):
    db.delete_address(address_id)
    return {"message": "Address deleted successfully"}

@app.get("/addresses/distance/")
def get_addresses_within_distance(latitude: float, longitude: float, distance: float):
    return db.get_addresses_within_distance(latitude, longitude, distance)
