import glob
import gzip
import os
import sys
import time as timed
from datetime import date, datetime, time, timedelta
from logging import Logger, getLogger, StreamHandler, Formatter, ERROR
from logging.handlers import TimedRotatingFileHandler
import pytz
import settings


class CustomTimedRotatingFileHandler(TimedRotatingFileHandler):
    def __init__(self, backupCountCompressed: int, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.backupCountCompressed = backupCountCompressed

    @staticmethod
    def delete_old_compressed_logs(
        directory: str, compressed_files_count_limit: int
    ) -> None:
        files = sorted(glob.glob(os.path.join(directory, "*.gz")), key=os.path.getmtime)
        for file in files[:-compressed_files_count_limit]:
            os.remove(file)

    def doRollover(self):
        """Delete compressed log files taking into account backupCountCompressed"""
        super().doRollover()
        directory = os.path.dirname(self.baseFilename)
        self.delete_old_compressed_logs(directory, self.backupCountCompressed)


class MoscowTimeFormatter(Formatter):
    def __init__(self, fmt=None, datefmt=None, *args, **kwargs) -> None:
        super().__init__(fmt=fmt, datefmt=datefmt, *args, **kwargs)

    def formatTime(self, record, datefmt=None):
        """Formatting the time so that the logs show Moscow time"""
        utc_time = datetime.utcfromtimestamp(record.created)
        msk_time = utc_time.astimezone(pytz.timezone("Europe/Moscow"))
        if datefmt:
            return msk_time.strftime(datefmt)
        return msk_time.isoformat()


class GetLogger:
    """Singleton class for getting logger"""

    _instance = None
    logger: Logger
    error_logs_path: str = settings.ERROR_LOG_PATH
    other_logs_path: str = settings.LOG_PATH

    # After 30 compressed log file, when new compressed log file will be created old will be deleted
    compressed_files_count_limit = 30
    # Same as with compressed_files_count_limit, but for not compressed log files
    not_compressed_files_count_limit = 1
    interval_create_new_log_file = 1
    encoding_log_files = "utf-8"
    when_create_new_log_file = "midnight"
    # MSK time
    rotation_time = time(23, 59, 59)
    logger_level = settings.LOG_LEVEL

    # Calculate the real rollover interval, which is just the number of
    # seconds between rollovers.  Also set the filename suffix used when
    # a rollover occurs.  Current 'when' events supported:
    # S - Seconds
    # M - Minutes
    # H - Hours
    # D - Days
    # midnight - roll over at midnight
    # W{0-6} - roll over on a certain day; 0 - Monday

    _formatter: MoscowTimeFormatter = MoscowTimeFormatter(
        fmt=(
            "%(asctime)s [%(levelname)s] [%(pathname)s:%(funcName)s: "
            "%(lineno)d]: %(message)s"
        )
    )

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self) -> None:
        if getattr(self, "logger", None) is None:
            self.logger = self.prepare_logger()

    @staticmethod
    def compress_old_log(log_filename: str, *args) -> None:
        """Function for compressing old log files"""
        today_date = date.today().strftime("%Y_%m_%d")
        compressed_filename = f"{os.path.dirname(log_filename)}/{today_date}.log.gz"

        with open(log_filename, "rb") as f_in:
            # compressed filename - filename.log.gz, because for gzip inside file it is a filename without gzip
            with gzip.open(compressed_filename, "wb") as f_out:
                f_out.writelines(f_in)

        os.remove(log_filename)

    def prepare_handler(
        self, level: int | str, path: str
    ) -> CustomTimedRotatingFileHandler:

        msk_datetime = datetime.combine(datetime.today(), self.rotation_time)
        utc_datetime = msk_datetime - timedelta(hours=3)
        utc_time = utc_datetime.time()

        handler = CustomTimedRotatingFileHandler(
            filename=f"{path}/today_logs.log",
            when=self.when_create_new_log_file,
            backupCount=self.not_compressed_files_count_limit,
            backupCountCompressed=self.compressed_files_count_limit,
            encoding=self.encoding_log_files,
            atTime=utc_time,
            utc=False,
        )

        # function for compressing file
        handler.rotator = self.compress_old_log
        handler.setFormatter(self._formatter)
        handler.setLevel(level)

        return handler

    def create_dirs(self):
        paths = [self.other_logs_path, self.error_logs_path]

        for path in paths:
            if not os.path.exists(path):
                os.makedirs(path)

    def prepare_logger(self) -> Logger:
        logger: Logger = getLogger(__name__)
        logger.setLevel(self.logger_level)

        if os.getenv("PYTEST") is not None:
            return logger

        self.create_dirs()

        stream_handler = StreamHandler(stream=sys.stdout)
        stream_handler.setFormatter(self._formatter)

        handler = self.prepare_handler(
            level=self.logger_level, path=self.other_logs_path
        )
        error_handler = self.prepare_handler(level=ERROR, path=self.error_logs_path)

        logger.addHandler(stream_handler)
        logger.addHandler(handler)
        logger.addHandler(error_handler)

        logger.info(
            f"Next rotation scheduled for: {datetime.utcfromtimestamp(handler.computeRollover(int(timed.time())))} UTC"
        )
        return logger


log = GetLogger().logger
