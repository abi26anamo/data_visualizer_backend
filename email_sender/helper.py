import sendgrid
from django.conf import settings
import base64
import pandas as pd
from sendgrid.helpers.mail import Mail, Email, To, Content, Attachment
# from .models import EmailsSender, EmailRecipient


def send_email(recipient_emails, subject, body, attachments):
    """
    Send email to individual recipients and bulk recipients.

    :param recipient_emails: List of individual recipient email addresses.
    :param subject: Subject of the email.
    :param body: Body content of the email.
    :param attachments: List of file attachments.
    :param bulk_recipients: List of bulk recipient email addresses.
    :return: True if email sent successfully, False otherwise.
    """

    for recipient_email in recipient_emails:
        email_body = body.replace("[name]", '')
        general_send_email(recipient_email, subject, email_body, attachments)
    return True


def general_send_email(recipient_email, subject, body, attachments):
    """
    Send email using SendGrid API.

    :param recipient_email: Email address of the recipient.
    :param subject: Subject of the email.
    :param body: Body content of the email.
    :param attachments: List of file attachments.
    """
    content = Content("text/html", body)
    sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
    to_email = To(recipient_email)
    from_email = Email("info@trounceflow.com", "Trounceflow")
    mail = Mail(from_email, to_email, subject, content)

    for attachment in attachments:
        mail.attachment = Attachment(
            base64.b64encode(attachment.read()).decode(),
            attachment.name,
            attachment.content_type)

    # Get a JSON-ready representation of the Mail object
    mail_json = mail.get()

    # Send an HTTP POST request to /mail/send
    sg.client.mail.send.post(request_body=mail_json)


# def save_email(recipient_emails, subject, body, attachments, bulk_recipients):
#     """
#     Save email details to the database.

#     :param recipient_emails: List of individual recipient email addresses.
#     :param subject: Subject of the email.
#     :param body: Body content of the email.
#     :param attachments: List of file attachments.
#     :param bulk_recipients: List of bulk recipient email addresses.
#     """
#     email_data = {"subject": subject}
#     email = EmailsSender.objects.create(**email_data)

#     if email:
#         # save recepients
#         for recipient_email in recipient_emails:
#             recepient = {"email_address": recipient_email, "emails_sender": email}
#             EmailRecipient.objects.create(**recepient)

#         # save attachments
#         # for attachment in attachments:
#             # pass

#         # if bulk attached
#         for recipient_email in bulk_recipients:
#             if len(recipient_email) > 0:
#                 recepient = {"email_address": recipient_email[0], "emails_sender": email}
#                 EmailRecipient.objects.create(**recepient)


def read_uploaded_excel(excel_file):
    """
    Read data from an uploaded Excel file.

    :param excel_file: Uploaded Excel file.
    :return: List of lists containing Excel data if successful, False otherwise.
    """
    try:
        if excel_file and len(excel_file) > 0:
            if '.' in excel_file.name and excel_file.name.split('.')[-1].lower() in ["xlsx", "xsl", "csv"]:
                if excel_file.name.split('.')[-1].lower() == 'csv':
                    # Read the CSV file into a pandas DataFrame
                    df = pd.read_csv(excel_file)

                else:
                    # Read the Excel file into a pandas DataFrame
                    df = pd.read_excel(excel_file)

                # Convert the DataFrame to a list of lists
                excel_data = df.values.tolist()

                return excel_data
            else:
                return 'False'

        return []
    except Exception:
        return 'False'
