from fastapi import APIRouter, HTTPException
from src.api.dependencies import DBDep
from src.exeptions import ObjectNotFoundException, AllRoomsAreBookedException, RoomNotFoundHTTPException, \
    RoomNotFoundException, AllRoomsAreBookedHTTPException

from src.schemas.bookings import BookingAdd
from src.api.dependencies import UserIdDep
from src.services.bookings import BookingService

router = APIRouter(prefix="/bookings", tags=["Бранирования"])


@router.get("")
async def get_bookings(db: DBDep):
    return await BookingService(db).get_bookings()

@router.get("/me")
async def get_my_bookings(user_id: UserIdDep, db: DBDep):
    return await BookingService(db).get_my_bookings(user_id=user_id)


@router.post("")
async def add_booking(
        user_id: UserIdDep,
        booking_data: BookingAdd,
        db: DBDep
):
    try:
        booking = await BookingService(db).add_booking(user_id=user_id, booking_data=booking_data)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except AllRoomsAreBookedException:
        raise AllRoomsAreBookedHTTPException

    return {"status_code": 200, "data": booking}

