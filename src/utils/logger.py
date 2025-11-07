import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Optional: Add a console handler if not already present
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
