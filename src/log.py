import logging

def setup_custom_logger(name):
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logging.basicConfig(filename=name,
                    filemode='a',
                    level=logging.DEBUG)

    logger = logging.getLogger(name)
    logger.addHandler(handler)

    logger.debug(f"[INFO]: Logger {name} setup")

    return logger