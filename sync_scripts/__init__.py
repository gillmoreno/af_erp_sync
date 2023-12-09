import sys
from loguru import logger
import datetime

now_string = str(datetime.datetime.now())

logger.basicConfig(
    level=logger.INFO,
    filename=f"logs/{format(now_string)}-sync.log",
    filemode="w",
    format="%(name)s - %(levelname)s - %(message)s",
)

root = logger.getLogger()
root.setLevel(logger.INFO)

handler = logger.StreamHandler(sys.stdout)
handler.setLevel(logger.INFO)
formatter = logger.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
root.addHandler(handler)
