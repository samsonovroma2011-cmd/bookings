from datetime import timedelta, datetime, timezone

from fastapi import HTTPException
from passlib.context import CryptContext
import jwt

from src.config import settings
from src.exeptions import ObjectAlreadyExistsException, UserAlreadyExistsException, IncorrectPasswordException, \
    IncorrectAccessTokenException, EmailNotRegisteredException
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.base import BaseService


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode |= {"exp": expire}
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def encode_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        except jwt.exceptions.DecodeError:
            raise IncorrectAccessTokenException

    async def register_user(
            self,
            data: UserRequestAdd
    ):
        hashed_password = self.hash_password(data.password)
        new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)

        try:
            user_data = await self.db.users.add_user(new_user_data)
        except ObjectAlreadyExistsException as ex:
            raise UserAlreadyExistsException from ex

        await self.db.commit()

        return user_data

    async def login_user(
            self,
            data: UserRequestAdd,

    ):
        user = await self.db.users.get_user_with_hashed_password(email=data.email)
        if not user:
            raise EmailNotRegisteredException
        if not self.verify_password(data.password, user.hashed_password):
            raise IncorrectPasswordException
        access_token = self.create_access_token({"user_id": user.id})

        return access_token

    async def get_me(
            self,
            user_id
    ):
        user = await self.db.users.get_one_or_none(id=user_id)
        return user



