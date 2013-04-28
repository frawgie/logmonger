import sys
sys.path.append("..")

import logging
import logmonger

logger = logging.getLogger()

handler = logmonger.MongoHandler()
logger.addHandler(handler)

logger.critical("My critical")
logger.error("My error")
logger.warning("My warning")
logger.info("My notification")
logger.debug("My debug")
logger.exception(Exception("My exception"))

