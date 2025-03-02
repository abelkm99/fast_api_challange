import logging

from app.config import MySettings


class CustomLogger:
    @classmethod
    def setup_logger(cls):
        logging.basicConfig(level=logging.DEBUG)
        logger = logging.getLogger("fastapi-backend-logger")

        logger.setLevel(logging._nameToLevel.get(MySettings.LOG_LEVEL, logging.INFO))
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    @staticmethod
    def get_logger():
        return logging.getLogger("fastapi-backend-logger")

    @staticmethod
    def add_handler(handler):
        logger = logging.getLogger("fastapi-backend-logger")
        logger.addHandler(handler)
