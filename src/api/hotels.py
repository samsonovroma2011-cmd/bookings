from datetime import date

from fastapi import APIRouter, Body, Query
from fastapi_cache.decorator import cache

from src.exeptions import ObjectNotFoundException, HotelNotFoundHTTPException
from src.schemas.hotels import HotelPatch, HotelAdd
from src.api.dependencies import PaginationDep, DBDep
from src.services.hotels import HotelService

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
@cache(expire=10)
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        location: str | None = Query(None, description="Адрес"),
        title: str | None = Query(None, description="Название отеля"),
        date_from: date = Query(examples="2026-07-01"),
        date_to: date = Query(examples="2026-07-10")
):
    return await HotelService(db).get_hotels(
            pagination=pagination,
            location=location,
            title=title,
            date_from=date_from,
            date_to=date_to
    )

@router.get("/{hotels_id}")
@cache(expire=10)
async def get_hotel_by_id(hotel_id: int, db: DBDep):
    try:
        return await HotelService(db).get_hotel(hotel_id=hotel_id)
    except ObjectNotFoundException as ex:
        raise HotelNotFoundHTTPException from ex


@router.post("")
async def create_hotel(
        db: DBDep,
        hotel_data: HotelAdd = Body(
            openapi_examples={
                "1": {
                    "summary": "Сочи",
                    "value": {
                        "title": "Отель Сочи 5 звёзд у моря",
                        "location": "sochi_u_morya",
                    }
                },
                "2": {
                    "summary": "Дубай",
                    "value": {
                        "title": "Отель Дубай у фонтана",
                        "location": "dubai_fountain",
                    },
                },
            }
        )
):
    hotel = await HotelService(db).add_hotel(hotel_data=hotel_data)
    return {"status_code": 200, "data": hotel}

@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int, db: DBDep):
    await HotelService(db).delete_hotel(hotel_id=hotel_id)

    return {"status_code": 200}

@router.put("/{hotel_id}")
async def put_hotel(hotel_id: int, hotel_data: HotelAdd, db: DBDep):
    await HotelService(db).edit_hotel(hotel_id=hotel_id, hotel_data=hotel_data)
    return {"status_code": 200}

@router.patch("/{hotel_id}")
async def patch_hotel(hotel_id: int, hotel_data: HotelPatch, db: DBDep):
    await HotelService(db).edit_hotel_partially(hotel_id=hotel_id,hotel_data=hotel_data)
    return {"status_code": 200}