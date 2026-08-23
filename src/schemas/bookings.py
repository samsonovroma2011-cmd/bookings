from pydantic import BaseModel, ConfigDict
from datetime import date


class BookingAdd(BaseModel):
    room_id: int
    date_from: date
    date_to: date

class BookingTest(BookingAdd):
    user_id: int
    price: int

class Booking(BookingAdd):
    id: int
    user_id: int
    price: int

    model_config = ConfigDict(from_attributes=True)