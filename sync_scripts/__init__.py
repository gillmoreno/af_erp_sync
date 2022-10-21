import sys
import logging
import datetime

now_string = str(datetime.datetime.now())

logging.basicConfig(
    level=logging.INFO,
    filename=f"logs/{format(now_string)}-sync.log",
    filemode="w",
    format="%(name)s - %(levelname)s - %(message)s",
)

root = logging.getLogger()
root.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
root.addHandler(handler)
