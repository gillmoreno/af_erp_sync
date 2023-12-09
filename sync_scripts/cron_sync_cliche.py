import os, sys
import time
from loguru import logger
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from apis.customers.customers_wp_apis import retrieve_customer
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

    start_time = time.time()
    logger.info("Start Create Cliche Images...")

    # Configurazione dell'accesso al sito Wordpress
    url = f"https://{os.environ.get('DOMAIN')}/xmlrpc.php"
    username = os.environ.get('WP_ADMIN')
    password = os.environ.get('WP_PASSWORD')
    client = Client(url, username, password)

    # logger.info("client -> {}".format(client))

    # query SAM_CLICHE
    query = f"""
        SELECT 
            szImmagineCliche, szCodiceCliente, szNoteCliche
        FROM 
            SAM_CLICHE
    """
    sam_cliches = query_sync_db(query, True)

    # logger.info("query DB {}".format(sam_cliches))

    if sam_cliches:

        for cliche in sam_cliches:

            # ID dell'utente a cui associare le immagini
            customer_id = int(cliche['szCodiceCliente'])

            check_customer_id = retrieve_customer(customer_id)

            logger.info('CHECK ID -> {}'.format(check_customer_id))

            # se id utente corrisponde alla mail di un customer registrato
            if 'email' in check_customer_id:

                image_name = cliche['szImmagineCliche']
                image_description = cliche['szNoteCliche']

                # URL dell'immagine
                image_url = f"https://{os.environ.get('DOMAIN')}/ftp_product_images/cliche_images/{image_name}"

                logger.info('FTP IMAGE URL -> {}'.format(image_url))

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

                        image_description = cliche['szNoteCliche']  

                        # Modifica descrizione e autore del post relativo all'immagine
                        url = f"https://{os.environ.get('DOMAIN')}/wp-json/wp-api/v1/cliche?image_id={str(response['id'])}&customer_id={str(customer_id)}&post_content={str(image_description)}"
                        
                        logger.info('REQUEST URL -> {}'.format(url))

                        requests.request("GET", url)

                        # Stampa il risultato
                        logger.info('Immagine caricata come allegato di WordPress ID {} e associata all\'utente ID {}'
                            .format(response['id'], customer_id))
                    else:
                        logger.info(
                            'Immagine già presente su Wordpress con ID -> {}'.format(cliche_id))
                else:
                    logger.info('Immagine non disponibile, status {}'.format(check_url_status))
            else:
                logger.info('User non esistente {}'.format(check_customer_id))
    else:
        logger.info("NO CLICHE TO SYNC\n...\n")
    
    logger.info(f"Sync cliches, tempo -> {str(time.time() - start_time)}")


if "__main__" in __name__:
    create_cliche_images()
