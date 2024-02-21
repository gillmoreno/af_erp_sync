"""
Configures and initializes the WooCommerce API client for making REST API calls to a WooCommerce site.

This script sets up the API client using authentication details (consumer key and secret) and the site URL,
all of which are read from environment variables. It is designed to be used by other modules in the system
that require communication with the WooCommerce REST API.

Attributes:
    wcapi (API): An instance of the WooCommerce API client, configured for making API calls to the specified
                 WooCommerce site. This instance is set up with query string authentication, a specific API
                 version ('wc/v3'), and a timeout setting.

Environment Variables:
    DOMAIN: The domain name of the WooCommerce site, without the protocol part.
    WP_KEY: The consumer key for WooCommerce REST API authentication.
    WP_SECRET: The consumer secret for WooCommerce REST API authentication.

Usage:
    Import the `wcapi` object from this module in other parts of the system to make authenticated REST API
    calls to the WooCommerce site.
"""

import os
from dotenv import load_dotenv
from woocommerce import API

cwd = os.getcwd()
env_folder = cwd.replace("apis", "")
load_dotenv(f"{env_folder}/.env")

wcapi = API(
    url=f"https://{os.environ.get('DOMAIN')}",
    consumer_key=os.environ.get("WP_KEY"),
    consumer_secret=os.environ.get("WP_SECRET"),
    version="wc/v3",
    query_string_auth=True,
    timeout=30,
)
