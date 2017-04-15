import logging
import logging.handlers


def setup_logger(file_location, file_log_level, terminal_log_level):
    logger = logging.getLogger(__name__.split('.')[0])
    logger.setLevel(logging.DEBUG)

    fh = logging.handlers.RotatingFileHandler(file_location, maxBytes=1024, backupCount=1)
    fh.setLevel(file_log_level.upper())
    fh_formatter = logging.Formatter('%(asctime)-15s %(levelname)s %(message)s')
    fh.setFormatter(fh_formatter)

    ch = logging.StreamHandler()
    ch.setLevel(terminal_log_level.upper())
    ch_formatter = logging.Formatter('%(message)s')
    ch.setFormatter(ch_formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)
