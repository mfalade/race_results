import logging


class CustomLogger():
    format = '[%(levelname)s] %(asctime)s >>  %(message)s'

    def __init__(self, option=None, logfile='logs.log'):
        self.logger = logging.getLogger(option)
        logging.basicConfig(
			filename=logfile,
            format=self.format,
            level=logging.DEBUG,
            datefmt='%H:%M:%S'
        )

    def info(self, *args):
        return self.logger.info(*args)

    def debug(self, *args):
        return self.logger.debug(*args)

    def warn(self, *args):
        return self.logger.warn(*args)

    def error(self, *args):
        return self.logger.error(*args, exc_info=True)

    def critical(self, *args):
        return self.logger.critical(*args)