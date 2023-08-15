import logging


def logging_setup():
    logging.basicConfig(
        format='%(asctime)s - %(process)d - %(levelname)s: %(message)s',
        level=logging.DEBUG,
        handlers=[
            logging.StreamHandler()
        ]
    )
