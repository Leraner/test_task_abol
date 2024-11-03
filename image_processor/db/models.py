from sqlalchemy.orm import DeclarativeBase
import datetime
import settings
import pytz


def date_now():
    return datetime.datetime.now(pytz.timezone(settings.TIMEZONE)).replace(tzinfo=None)


class Base(DeclarativeBase): ...
