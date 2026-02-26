import logging

def setup_logging_info():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("hospital_management.log"),
            logging.StreamHandler()
        ]
    )

def setup_logging_error():
    logging.basicConfig(
        level=logging.ERROR,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("hospital_management.log"),
            logging.StreamHandler()
        ]
    )