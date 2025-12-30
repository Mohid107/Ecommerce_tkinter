import logging
import os
import sys

def setup_logger(name="ShopEasy"):
    """
    Sets up a logger that outputs to both a file and the console.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # prevent adding handlers multiple times
    if logger.hasHandlers():
        return logger

    # Format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # File Handler
    log_file = "app.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# Create a default instance for easy import
app_logger = setup_logger()
