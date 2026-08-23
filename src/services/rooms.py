from datetime import date

from src.exeptions import check_date_to_after_date_from, HotelNotFoundException, ObjectNotFoundException, \
    RoomNotFoundException
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import RoomAdd, RoomPatch, Room
from src.services.base import BaseService
from src.services.hotels import HotelService


class RoomService(BaseService):
    async def get_filtered_by_time(
            self,
            hotel_id: int,
            date_from: date,
            date_to: date
    ):
        check_date_to_after_date_from(date_to, date_from)

        return await self.db.rooms.get_filtered_by_time(
            hotel_id=hotel_id,
            date_from=date_from,
            date_to=date_to
        )

    async def get_room(self, hotel_id: int, id: int):
        return await self.db.rooms.get_one_with_rels(hotel_id=hotel_id, id=id)

    async def create_room(self, hotel_id: int, room_data: RoomAdd):
        try:
            await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException as ex:
            raise HotelNotFoundException from ex

        room = await self.db.rooms.add(
            data=room_data,
            exclude={"facilities_ids"},
            hotel_id=hotel_id,
        )

        rooms_facility_data = [
            RoomFacilityAdd(
                room_id=room.id,  # type: ignore
                facility_id=f_id
            ) for f_id in room_data.facilities_ids
        ]
        await self.db.rooms_facilities.add_bulk(rooms_facility_data)
        await self.db.commit()

    async def delete_room(self, hotel_id: int, room_id: int):
        await HotelService(self.db).get_hotel_with_check(hotel_id=hotel_id)

        await self.get_room_with_check(room_id=room_id)

        await self.db.commit()

    async def edit_room(self, hotel_id: int, room_id: int, room_data: RoomAdd):
        await HotelService(self.db).get_hotel_with_check(hotel_id=hotel_id)

        await self.get_room_with_check(room_id=room_id)

        await self.db.rooms.edit(
            data=room_data,
            is_patch=True,
            exclude={"facilities_ids"},
            hotel_id=hotel_id,
            room_id=room_id
        )

        await self.db.rooms_facilities.set_room_facilities(
            room_id=room_id,
            facilities_ids=room_data.facilities_ids
        )

        await self.db.commit()

    async def patch_edit_room(
            self,
            hotel_id: int,
            room_id: int,
            room_data: RoomPatch
    ):
        await HotelService(self.db).get_hotel_with_check(hotel_id=hotel_id)

        await self.get_room_with_check(room_id=room_id)

        await self.db.rooms.edit(
            data=room_data,
            is_patch=True,
            exclude={"facilities_ids"},
            hotel_id=hotel_id,
            room_id=room_id
        )

        if room_data.facilities_ids is not None:
            await self.db.rooms_facilities.set_room_facilities(
                room_id=room_id,
                facilities_ids=room_data.facilities_ids
            )

        await self.db.commit()

    async def get_room_with_check(self, room_id: int) -> Room:
        try:
            return await self.db.rooms.get_one(id=room_id)
        except ObjectNotFoundException:
            raise RoomNotFoundException