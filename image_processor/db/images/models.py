import datetime

from sqlalchemy.orm import mapped_column, Mapped

from ..models import Base, date_now
import uuid


class ImageModel(Base):
    __tablename__ = 'images'
    __table_args__ = {"extend_existing": True}

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(unique=False, nullable=False)
    file_path: Mapped[str] = mapped_column(unique=True, nullable=False)
    upload_date: Mapped[datetime.datetime] = mapped_column(nullable=False, default=date_now)
    resolution: Mapped[str] = mapped_column(nullable=False)
    size: Mapped[int] = mapped_column(nullable=False)