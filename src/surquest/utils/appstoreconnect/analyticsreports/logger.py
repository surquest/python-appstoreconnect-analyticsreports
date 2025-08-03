import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(levelname)-8s - %(asctime)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)