from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from .models import UserModel
from sqlalchemy import select
from schemas import CreateUserSchemaRequest, DatabaseException


class AuthDAL:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def create_user(self, create_schema: CreateUserSchemaRequest) -> UserModel:

        new_user = UserModel(**create_schema.model_dump())

        try:
            self.db_session.add(new_user)
            await self.db_session.flush()
            await self.db_session.refresh(new_user)
        except IntegrityError as e:
            raise DatabaseException(e.args[0].split("DETAIL:  ")[1])

        return new_user

    async def get_user_by_email(self, email: str) -> UserModel | None:
        query = select(UserModel).where(UserModel.email == email)

        try:
            result = await self.db_session.execute(query)
        except IntegrityError as e:
            raise DatabaseException(e.args[0].split("DETAIL:  ")[1])

        row = result.scalar()
        if row is not None:
            return row
