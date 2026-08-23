from pydantic import EmailStr, BaseModel
from sqlalchemy import select, insert
from sqlalchemy.exc import IntegrityError

from src.exeptions import ObjectAlreadyExistsException
from src.repositories.base import BaseRepository
from src.models.users import UsersOrm
from src.repositories.mappers.mappers import UserDataMapper
from src.schemas.users import UserWithHashedPassword


class UsersRepository(BaseRepository):
    model = UsersOrm
    mapper = UserDataMapper # type: ignore

    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)

        model = result.scalars().one()

        return UserWithHashedPassword.model_validate(model)

    async def add_user(self, data: BaseModel):
        add_hotel_stmt = (
            insert(self.model)  # type: ignore
            .values(
                **data.model_dump()
            )
            .returning(self.model)  # type: ignore
        )
        try:
            result = await self.session.execute(add_hotel_stmt)
        except IntegrityError as ex:
            raise ObjectAlreadyExistsException from ex
        model = result.scalars().one()
        return self.mapper.map_to_domain_entity(model)
