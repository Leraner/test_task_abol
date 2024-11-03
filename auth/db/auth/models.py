from sqlalchemy.orm import Mapped, mapped_column

from ..models import Base
import uuid


class UserModel(Base):
    __tablename__ = 'users'
    __table_args__ = {"extend_existing": True}

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4())
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)