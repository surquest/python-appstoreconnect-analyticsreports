import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Prevent messages from propagating to the root logger
logger.propagate = False

# Add handler only if this logger has no direct handlers
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(levelname)-8s - %(asctime)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)