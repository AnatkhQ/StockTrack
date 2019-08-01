import logging.handlers
from config import DEBUG
logger = logging.getLogger("logger")
logger.setLevel(logging.DEBUG)


formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")


handler1 = logging.StreamHandler()
handler1.setLevel(logging.DEBUG)
handler1.setFormatter(formatter)
if DEBUG:
    logger.addHandler(handler1)

handler2 = logging.FileHandler(filename="logs/running.log",encoding='utf-8')
handler2.setLevel(logging.INFO)
handler2.setFormatter(formatter)
logger.addHandler(handler2)