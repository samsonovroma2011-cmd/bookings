from typing import Annotated
from datetime import date

from fastapi import APIRouter
from fastapi.params import Query, Body

from src.api.dependencies import DBDep
from src.exeptions import (
    check_date_to_after_date_from,
    ObjectNotFoundException,
    HotelNotFoundHTTPException,
    RoomNotFoundHTTPException, RoomNotFoundException, HotelNotFoundException
)


from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import RoomAdd, RoomPatch
from src.services.rooms import RoomService

router = APIRouter(prefix="/hotels", tags=["Номера"])

@router.get("/{hotel_id}/rooms")
async def get_rooms(
        hotel_id: int,
        db: DBDep,
        date_from: Annotated[date, Query(examples="2026-07-01")],
        date_to: Annotated[date, Query(examples="2026-07-10")]
):
    return await RoomService(db).get_filtered_by_time(
        hotel_id=hotel_id,
        date_from=date_from,
        date_to=date_to
    )

@router.get("/{hotel_id}/rooms/{id}")
async def get_room_by_id(hotel_id: int, id: int, db: DBDep):
    try:
        return await RoomService(db).get_room(hotel_id=hotel_id, id=id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException

@router.post("/{hotel_id}/rooms")
async def create_room(hotel_id: int, db: DBDep, room_data: Annotated[RoomAdd, Body()]):
    try:
        room = await RoomService(db).create_room(hotel_id=hotel_id, room_data=room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException

    return {"status_code": 200, "data": room}

@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    try:
        await RoomService(db).delete_room(hotel_id=hotel_id, room_id=room_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException

    return {"status_code": 200}

@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_room(hotel_id: int, room_id: int, room_data: RoomAdd, db: DBDep):
    try:
        await RoomService(db).edit_room(
            hotel_id=hotel_id,
            room_id=room_id,
            room_data=room_data
        )
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException

    return {"status_code": 200}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def patch_edit_room(
        hotel_id: int,
        room_id: int,
        db: DBDep,
        room_data: RoomPatch
):
    try:
        await RoomService(db).patch_edit_room(
            hotel_id=hotel_id,
            room_id=room_id,
            room_data=room_data
        )
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException

    return {"status_code": 200}
