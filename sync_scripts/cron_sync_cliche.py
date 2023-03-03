import os, sys
import time
import logging

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from apis.db_queries import get_products_out_of_sync
from apis.products.products__common import *
from apis.products.products_wp_apis import *
from apis.sql import query_sync_db

import requests
import urllib.request
# pip install python-wordpress-xmlrpc   
from wordpress_xmlrpc import Client
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, users
from wordpress_xmlrpc.exceptions import InvalidCredentialsError


def create_cliche_images():

    print("Start Create Cliche Images")

    # Configurazione dell'accesso al sito Wordpress
    url = 'https://arturofacchini.it/xmlrpc.php'
    username = 'estroDev'
    password = 'vC^TsOj80#WI'
    client = Client(url, username, password)

    print("Client")

    # ID dell'utente a cui associare le immagini
    user_id = 61

    # URL dell'immagine
    image_url = 'https://arturofacchini.it/ftp_product_images/cliche_images/00007866_76.jpg'

    check_url_status = get_url_status(image_url)

    if check_url_status == "200":

        # prepare metadata
        data = {
            'name': 'picture.jpg',
            'type': 'image/jpeg',  # mimetype
            'author': user_id,
            'overwrite': True
        }

        # read the binary file and let the XMLRPC library encode it into base64
        with urllib.request.urlopen(image_url) as img:
            data['bits'] = xmlrpc_client.Binary(img.read())

        response = client.call(media.UploadFile(data))

        # Modifica l'autore del post relativo all'immagine
        url = f"https://arturofacchini.it/wp-json/wp-api/v1/cliche?image_id={str(response['id'])}&user_id={str(user_id)}"
        cliche_response = requests.request("GET", url)

        # logging.info(f"cliche response -> {str(cliche_response)}")

        # Stampa il risultato
        print('Immagine caricata come allegato di WordPress ID {} e associata all\'utente ID {}'
              .format(response['id'], user_id))
        # logging.info(
        #     f"Immagine caricata come allegato di WordPress ID {str(response['id'])} e associata all\'utente ID {str(user_id)}")
    else:
        print('Immagine non dispobile, status {}'.format(check_url_status))
        # logging.info(f"Immagine non dispobile, status {str(check_url_status)}")


# def get_url_status(url):  # checks status for url

#     try:
#         r = requests.get(url)
#         status_code = str(r.status_code)
#         # logging.info(f"image URL status -> {status_code}")

#     except Exception as e:
#         status_code = ""
#         # logging.info(f"image URL EXCEPTION -> {str(e)}")

#     return status_code


# def get_image_id_by_name(image_name: str):
#     url = f"https://arturofacchini.it/wp-json/wc/v3/image?image_name={image_name}"
#     image_id = requests.request("GET", url).json()
#     return image_id



if "__main__" in __name__:
    create_cliche_images()
