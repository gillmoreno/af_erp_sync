import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = "smtp..."
PORT = 465
SENDER_EMAIL = "x@arturofacchini.it"
PASSWORD = "PASSWORD"

FOOTER_EMAIL = "\n\nCordialmente,\nIl team di Arturo Facchini."

activate_account_email = lambda contact_name, company_name: {
    "subject": "Attivazione account Arturo Facchini",
    "text": f"Ciao {contact_name}, \n\n L'account per l'azienda {company_name} dentro il sito di Arturo Facchini \
        è attivo. Puoi accedere con questa mail e la tua password.{FOOTER_EMAIL}",
    "html": f"""
        <html>
            <body>
                <p>Ciao {contact_name},<br><br>
                L'account per l'azienda {company_name} dentro il sito di Arturo Facchini è attivo.
                Puoi accedere <a href="http://shop.arturofacchini.it">da questo link</a>
                con la tua mail e la password di registrazione.{FOOTER_EMAIL}
                </p>
            </body>
        </html>
    """
}

def send_email(receiver_email, email_content, is_test=False):
    message = MIMEMultipart("alternative")
    message["Subject"] = email_content["subject"]
    message["From"] = SENDER_EMAIL
    message["To"] = receiver_email

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(email_content["text"], "plain")
    part2 = MIMEText(email_content["html"], "html")

    if is_test:
        print(part2)
        return

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_SERVER, PORT, context=context) as server:
        server.login(SENDER_EMAIL, PASSWORD)
        server.sendmail(
            SENDER_EMAIL, receiver_email, message.as_string()
        )
    