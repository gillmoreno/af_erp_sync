import os, sys
import time
import logging
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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

load_dotenv(f"../.env")


def create_cliche_images():

    print("Start Create Cliche Images")

    # Configurazione dell'accesso al sito Wordpress
    url = f"https://{os.environ.get('DOMAIN')}/xmlrpc.php"
    username = os.environ.get('WP_ADMIN')
    password = os.environ.get('WP_PASSWORD')
    client = Client(url, username, password)

    # print("client -> {}".format(client))

    # query SAM_CLICHE
    query = f"""
        SELECT 
            szImmagineCliche, szCodiceCliente
        FROM 
            SAM_CLICHE
    """
    sam_cliches = query_sync_db(query, True)

    # print("query DB {}".format(sam_cliches))

    if sam_cliches:

        for cliche in sam_cliches:

            # ID dell'utente a cui associare le immagini
            user_id = int(cliche['szCodiceCliente'])
            image_name = cliche['szImmagineCliche']

            # URL dell'immagine
            image_url = f"https://arturofacchini.it/ftp_product_images/cliche_images/{image_name}"

            check_url_status = get_url_status(image_url)

            if check_url_status == "200":

                cliche_id = get_image_id_by_name(image_name)
                
                if (cliche_id == 0):

                    # prepare metadata
                    data = {
                        'name': image_name,
                        'type': 'image/jpeg',  # mimetype
                    }

                    # read the binary file and let the XMLRPC library encode it into base64
                    with urllib.request.urlopen(image_url) as img:
                        data['bits'] = xmlrpc_client.Binary(img.read())

                    response = client.call(media.UploadFile(data))

                    # Modifica l'autore del post relativo all'immagine
                    url = f"https://arturofacchini.it/wp-json/wp-api/v1/cliche?image_id={str(response['id'])}&user_id={str(user_id)}"
                    requests.request("GET", url)

                    # Stampa il risultato
                    print('Immagine caricata come allegato di WordPress ID {} e associata all\'utente ID {}'
                          .format(response['id'], user_id))
                else:
                    print(
                        'Immagine già presente su Wordpress con ID -> {}'.format(cliche_id))
            else:
                print('Immagine non dispobile, status {}'.format(check_url_status))
    else:
        print("NO CLICHE TO SYNC\n...\n")


if "__main__" in __name__:
    create_cliche_images()
