from sqlalchemy.ext.asyncio import AsyncSession
from ..database_conn import DatabaseConnection
from .dal import AuthDAL
from schemas import CreateUserSchemaRequest, UserDbSchema


class AuthHandlers(DatabaseConnection):
    @DatabaseConnection.create_session
    async def create_user(
        self, create_schema: CreateUserSchemaRequest, db_session: AsyncSession
    ) -> UserDbSchema:
        auth_dal = AuthDAL(db_session)
        created_user = await auth_dal.create_user(create_schema)
        return UserDbSchema.model_validate(
            created_user, context={"_hashed_password": created_user.hashed_password}
        )

    @DatabaseConnection.create_session
    async def get_user_by_email(
        self, email: str, db_session: AsyncSession
    ) -> UserDbSchema | None:
        auth_dal = AuthDAL(db_session)
        user = await auth_dal.get_user_by_email(email=email)
        if user is not None:
            return UserDbSchema.model_validate(
                user, context={"_hashed_password": user.hashed_password}
            )
