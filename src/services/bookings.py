from src.exeptions import ObjectNotFoundException, RoomNotFoundHTTPException, AllRoomsAreBookedException, \
    RoomNotFoundException
from src.schemas.bookings import BookingAdd
from src.services.base import BaseService


class BookingService(BaseService):
    async def get_bookings(self):
        return await self.db.bookings.get_all()

    async def get_my_bookings(self, user_id):
        return await self.db.bookings.get_filtered(user_id=user_id)

    async def add_booking(
            self,
            user_id,
            booking_data: BookingAdd,
    ):
        try:
            room = await self.db.rooms.get_one(id=booking_data.room_id)
        except ObjectNotFoundException:
            raise RoomNotFoundException

        days = (booking_data.date_to - booking_data.date_from).days
        total_cost = room.price * days  # type: ignore

        try:
            booking = await self.db.bookings.add_booking(data=booking_data, user_id=user_id, price=total_cost)
        except AllRoomsAreBookedException as ex:
            raise ex

        await self.db.commit()

        return booking