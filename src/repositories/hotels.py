from datetime import date

from sqlalchemy import select

from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.models.hotels import HotelsOrm
from src.repositories.mappers.mappers import HotelDataMapper
from src.repositories.utils import room_ids_for_booking
from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    mapper = HotelDataMapper # type: ignore

    async def get_all(
            self,
            location: str | None = None,
            title: str | None = None,
            page: int = 1,
            per_page: int = 5
    ) -> list[Hotel]:

        query = select(self.model)
        if location:
            query = query.filter(self.model.location.ilike(f"%{location.strip()}%"))
        if title:
            query = query.filter(self.model.title.ilike(f"%{title.strip()}%"))
        query = query.limit(per_page).offset((page - 1) * per_page)
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]

    async def get_filtered_by_time(
            self,
            date_from: date,
            date_to: date,
            location: str | None = None,
            title: str | None = None,
            page: int = 1,
            per_page: int = 5
    ):



        rooms_ids_to_get = room_ids_for_booking(date_from=date_from, date_to=date_to)

        hotels_ids_to_get = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )

        if location:
            hotels_ids_to_get = hotels_ids_to_get.filter(self.model.location.ilike(f"%{location.strip()}%"))
        if title:
            hotels_ids_to_get = hotels_ids_to_get.filter(self.model.title.ilike(f"%{title.strip()}%"))
        hotels_ids_to_get = (
            hotels_ids_to_get
            .limit(per_page)
            .offset((page - 1) * per_page)
        )

        return await self.get_filtered(self.model.id.in_(hotels_ids_to_get))

