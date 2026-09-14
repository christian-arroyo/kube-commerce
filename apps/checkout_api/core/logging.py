import logging

def setup_logging(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"):
    logging.basicConfig(
        level=level,
        format=format
    )
