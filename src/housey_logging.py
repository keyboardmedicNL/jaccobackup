import logging


def configure():
    logging.basicConfig(
        format='%(asctime)s %(levelname)s: [%(module)s.%(funcName)s:%(lineno)d]: %(message)s',
        filename='./jacco_backup.log',
        level=logging.DEBUG
    )

    console = logging.StreamHandler()
    console.setLevel(level=logging.DEBUG)
    console.setFormatter(
        logging.Formatter('%(asctime)s %(levelname)s: [%(module)s.%(funcName)s:%(lineno)d]: %(message)s')
    )
    logging.getLogger().addHandler(console)

