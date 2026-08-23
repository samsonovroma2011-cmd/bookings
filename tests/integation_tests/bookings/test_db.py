from datetime import date

from src.schemas.bookings import BookingTest


async def test_booking_crud(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id

    booking_data = BookingTest(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2026, month=8, day=10),
        date_to=date(year=2026, month=8, day=20),
        price=100
    )
    booking_add = await db.bookings.add(booking_data)

    get_booking = await db.bookings.get_one_or_none(id=booking_add.id)
    assert get_booking

    edit_data = BookingTest(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2026, month=8, day=10),
        date_to=date(year=2026, month=8, day=20),
        price=50
    )

    await db.bookings.edit(data=edit_data, id=booking_add.id)

    get_edit_booking = await db.bookings.get_one_or_none(id=booking_add.id)
    assert get_edit_booking
    assert get_edit_booking != get_booking

    await db.bookings.delete(id=booking_add.id)

    delete_booking = await db.bookings.get_one_or_none(id=booking_add.id)
    assert not delete_booking

    await db.commit()