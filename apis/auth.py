import os
from dotenv import load_dotenv
from woocommerce import API

cwd = os.getcwd()
env_folder = cwd.replace('apis', '')
load_dotenv(f'{env_folder}/.env')

wcapi = API(
    url="https://dev.arturofacchini.it",
    consumer_key=os.environ.get("WP_KEY"),
    consumer_secret=os.environ.get("WP_SECRET"),
    version="wc/v3",
    query_string_auth=True
)