import logging
from typing import Sequence

from asyncpg import UniqueViolationError
from sqlalchemy.exc import NoResultFound, IntegrityError
from pydantic import BaseModel
from sqlalchemy import select, insert, delete, update

from src.exeptions import ObjectNotFoundException, ObjectAlreadyExistsException
from src.repositories.mappers.base import DataMapper


class BaseRepository:
    model = None # type: ignore
    mapper: DataMapper = None # type: ignore

    def __init__(self, session):
        self.session = session

    async def get_filtered(self, *filter, **filter_by):
        query = (
            select(self.model) # type: ignore
            .filter(*filter)
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]

    async def get_all(self):
       return await self.get_filtered()


    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by) # type: ignore
        result = await self.session.execute(query)

        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.mapper.map_to_domain_entity(model)

    async def get_one(self, **filter_by):
        query = select(self.model).filter_by(**filter_by) # type: ignore
        result = await self.session.execute(query)

        try:
            model = result.scalars().one()
        except NoResultFound as ex:
            raise ObjectNotFoundException from ex

        return self.mapper.map_to_domain_entity(model)


    async def add(self, data: BaseModel, exclude: set[str] | dict | None = None, **kwargs):
        try:
            add_hotel_stmt = (
                insert(self.model) # type: ignore
                .values(
                    **data.model_dump(exclude=exclude),
                    **kwargs
                )
                .returning(self.model) # type: ignore
            )

            result = await self.session.execute(add_hotel_stmt)
            model = result.scalars().one()
            return self.mapper.map_to_domain_entity(model)
        except IntegrityError as ex:
            logging.error(
                 f"Не удалось добавить данные в БД, входные данные={data} тип ошибки:{type(ex.orig.__cause__)=}"
             )
            if isinstance(ex.orig.__cause__, UniqueViolationError):
                raise ObjectAlreadyExistsException from ex
            else:
                logging.error(f"Незнакомая ошибка, входные данные={data} тип ошибки:{type(ex.orig.__cause__)=}")
                raise ex


    async def add_bulk(self, data: Sequence[BaseModel], exclude: dict | None = None, **filter_by):
        model_dump_data = [item.model_dump(exclude=exclude) for item in data]
        add_hotel_stmt = insert(self.model).values(model_dump_data, **filter_by) # type: ignore
        await self.session.execute(add_hotel_stmt)

    async def edit(
            self,
            data: BaseModel,
            is_patch: bool = False,
            exclude: set[str] | dict | None = None,
            **filter_by
    ) -> None:
        update_stmt = (
            update(self.model) # type: ignore
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=is_patch, exclude=exclude))
        )
        await self.session.execute(update_stmt)


    async def delete(self, *filter, **filter_by) -> None:
        delete_stmt = delete(self.model).filter(*filter).filter_by(**filter_by) # type: ignore
        await self.session.execute(delete_stmt)

