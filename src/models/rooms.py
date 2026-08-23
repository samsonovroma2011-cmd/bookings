import typing

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

from src.database import Base
from src.models.facilities import FacilitiesOrm

if typing.TYPE_CHECKING:
    from src.models import FacilitiesOrm

class RoomsOrm(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    title: Mapped[str]
    description: Mapped[str | None] = mapped_column(nullable=True)
    price: Mapped[int]
    quantity: Mapped[int]

    facilities: Mapped[list["FacilitiesOrm"]] = relationship(
        back_populates="rooms",
        secondary="rooms_facilities"
    )