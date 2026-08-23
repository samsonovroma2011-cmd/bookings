from datetime import date

from sqlalchemy import select, func

from src.exeptions import AllRoomsAreBookedException
from src.models import RoomsOrm
from src.repositories.base import BaseRepository
from src.models.bookings import BookingsOrm
from src.repositories.mappers.mappers import BookingDataMapper
from src.schemas.bookings import BookingAdd


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper # type: ignore

    async def get_bookings_with_today_checkin(self):
        query = (
            select(self.model)
            .filter(self.model.date_from == date.today())
        )
        res = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()]


    async def add_booking(self, data: BookingAdd, **filter_by):
        query_bookings = (
            select(func.count('*')).
            select_from(self.model)
            .filter(
        self.model.room_id == data.room_id,
                self.model.date_from <= data.date_to,
                self.model.date_to >= data.date_from
            )
        )
        booking_count = (await self.session.execute(query_bookings)).scalars().one()

        query_rooms = (
            select(RoomsOrm.quantity)
            .select_from(RoomsOrm)
            .filter_by(id=data.room_id)
        )
        room_quantity = await self.session.scalar(query_rooms)

        if booking_count >= room_quantity:
            raise AllRoomsAreBookedException

        return await self.add(data=data, **filter_by)