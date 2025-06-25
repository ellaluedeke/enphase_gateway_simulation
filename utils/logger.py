import logging
import os

LOG_FILE = "attack_log.txt"

# Create logs directory if it doesn't exist
if not os.path.exists("logs"):
    os.makedirs("logs")

# Setting up the logger
logging.basicConfig(
    level=logging.DEBUG,  # Log everything (DEBUG and above)
    format="%(asctime)s [%(levelname)s] - %(message)s",
    handlers=[
        logging.FileHandler(f"logs/{LOG_FILE}"),
        logging.StreamHandler()  # Also output logs to the console
    ]
)

# Logger object
logger = logging.getLogger()

# Function to log message
def log_message(message, level="INFO"):
    if level == "DEBUG":
        logger.debug(message)
    elif level == "INFO":
        logger.info(message)
    elif level == "WARNING":
        logger.warning(message)
    elif level == "ERROR":
        logger.error(message)
    elif level == "CRITICAL":
        logger.critical(message)
