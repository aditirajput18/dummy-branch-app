import logging
from pythonjsonlogger import jsonlogger


logger = logging.getLogger("loan-api")
logger.setLevel(logging.INFO)


if not logger.handlers:
handler = logging.StreamHandler()
fmt = "%(asctime)s %(levelname)s %(name)s %(message)s %(request_id)s"
formatter = jsonlogger.JsonFormatter(fmt)
handler.setFormatter(formatter)
logger.addHandler(handler)


# Provide convenience functions
def get_logger():
return logger
