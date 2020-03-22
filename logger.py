import logging


class Logger:
    # loggerはSingleton
    def __new__(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.fmt = "%(asctime)s %(levelname)s %(name)s : %(message)s"
        logging.basicConfig(level=logging.INFO, format=self.fmt)

    def info(self, message):
        self.logger.info(message)

    def warn(self, message):
        self.logger.warn(message)

    def error(self, message, exception, exc_info=True):
        self.logger.error(message, exception, exc_info)
