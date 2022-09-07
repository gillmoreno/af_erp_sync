#!/usr/local/bin/python3
from smtp_email import *
from sql import query_sync_db

"""
[] Utente registrato da WP fa partire email interna per notificare il responsabile
   che un nuovo utente si è registrato e bisogna attivare l'account 
   #TODO[API WP]
[x] Una volta il responsabile attiva l'account (tramite is_wp_active) viene inviata
   una mail all'utente per indicarli che può accedere al suo account. 
[] Sincronizza informazione del prodotto (Sempre dal gestionale -> WP)
    [] Crea prodotto wu WP
    [] Sincronizza prodotto su WP
[] Quando viene fatto l'ordine online, oltre alla mail per il cliente, arriva una mail
   per il responsabile 
   #TODO[API WP]
[] Dissattiva account da gestionale (is_wp_active) / o WP #TODO[Aggancio WP]
[] Aggancia ordine dall'ERP con l'ordine di WP
[] Sincronizza stato dell'ordine
"""

def notify_responsible_about_new_accounts():
    # TODO[Aggancio WP]
    # Una view sul gestionale per utenti non WP_ACTIVE (forse aggiungere il campo eliminati)
    # Questo per evitare di inviare tante email di nuovo account (ogni crontab)
    pass

def send_account_activated_emails():
    query = """
    SELECT id_wp, email, contact_name, company_name FROM customers
    WHERE id_sam_erp IS NULL AND NOT activation_email_sent=1
    """
    mails_to_send = query_sync_db(query)
    wp_ids = []
    for (id_wp, email, contact_name, company_name) in mails_to_send:
        send_email(
            email=email,
            email_content=activate_account_email(contact_name, company_name),
            is_test=True
        )
        wp_ids.append(id_wp)
    update_activation_email_sent(wp_ids)

def update_activation_email_sent(wp_ids):
    if len(wp_ids) > 1:
        update_query = f"UPDATE customers SET activation_email_sent=1 WHERE customers.id_wp IN {str(tuple(wp_ids))};"
    else:
        update_query = f"UPDATE customers SET activation_email_sent=1 WHERE customers.id_wp={wp_ids[0]};"    
    query_sync_db(update_query, True)


def send_internal_email_for_new_order():
    # TODO[Aggancio WP]
    pass

def deactivate_account_from_erp():
    pass


send_account_activated_emails()