from pydantic import BaseModel, ConfigDict
from src.schemas.facilities import Facility

class RoomBase(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int

class RoomTest(RoomBase):
    hotel_id: int

class RoomAdd(RoomBase):
    facilities_ids: list[int] = []

class Room(RoomBase):
    id: int
    hotel_id: int
    model_config = ConfigDict(from_attributes=True)

class RoomWithRels(Room):
    facilities: list[Facility]

class RoomPatch(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
    facilities_ids: list[int] | None = None