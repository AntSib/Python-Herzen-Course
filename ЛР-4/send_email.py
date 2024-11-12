import smtplib
from secrets import sender, receiver, google_app_password
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_test_email(sender: str, receiver: str, password: str, subject: str, body: str) -> None:
    """
    Sends a email from the given sender to the receiver with the specified subject and body.

    :param str sender: The email address of the sender.
    :param str receiver: The email address of the receiver.
    :param str password: The password for the sender's email account.
    :param str subject: The subject of the email.
    :param str body: The body content of the email.

    :returns: None

    :raises Exception: If any error occurs during the email sending process.
    """
    port = 465

    msg = MIMEMultipart()           # Using MIMEMultipart to assemble the email
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain')) # Attaching the body to the email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', port) as server:    # Setting up the server
            server.ehlo()
            server.login(sender, password)                          # Logging in via google apps password
            server.sendmail(sender, receiver, msg.as_string())      # Sending the email
    except Exception as e:              # to catch random exceptions
        print(f"Error: {e}")


if __name__ == "__main__":
    subject = "Python test email"
    body = "This is a test email sent via Python."

    send_test_email(sender, receiver, google_app_password, subject, body)
