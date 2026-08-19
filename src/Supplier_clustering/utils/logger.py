import os # creates directories and handles file paths
import sys
import logging

logging_str = "[%(asctime)s: %(levelname)s: %(module)s: %(message)s]"

log_dir = "logs"
log_filepath = os.path.join(log_dir, "running_logs.log")

os.makedirs(log_dir, exist_ok=True)

logger = logging.getLogger("mlProjectLogger")
logger.setLevel(logging.INFO)

if not logger.handlers:
    file_handler = logging.FileHandler(log_filepath) # Write logging messages to logs/running_logs.log.
    stream_handler = logging.StreamHandler(sys.stdout) # Print logging messages to the console or terminal (stdout).

    file_handler.setFormatter(logging.Formatter(logging_str))
    stream_handler.setFormatter(logging.Formatter(logging_str))

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)