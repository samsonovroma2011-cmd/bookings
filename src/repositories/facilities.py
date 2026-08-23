from sqlalchemy import select, delete, insert

from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import FacilityDataMapper, RoomFacilityDataMapper

from src.schemas.facilities import Facility, RoomFacility


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    mapper = FacilityDataMapper # type: ignore


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    mapper = RoomFacilityDataMapper # type: ignore

    async def set_room_facilities(self, room_id: int, facilities_ids: list[int]):
        get_current_facilities_ids = (
            select(self.model.facility_id)
            .filter_by(room_id=room_id)
        )

        res = await self.session.execute(get_current_facilities_ids)
        current_facilities_ids: list[int] = res.scalars().all()
        to_delete: list[int] = list(set(current_facilities_ids) - set(facilities_ids))
        to_insert: list[int] = list(set(facilities_ids) - set(current_facilities_ids))

        if to_delete:
            delete_stmt = (
                delete(self.model)
                .filter(
                    self.model.room_id == room_id,
                    self.model.facility_id.in_(to_delete)
                )
            )
            await self.session.execute(delete_stmt)

        if to_insert:
            insert_stmt = (
                insert(self.model)
                .values([{"room_id": room_id, "facility_id": f_id} for f_id in to_insert])
            )
            await self.session.execute(insert_stmt)

