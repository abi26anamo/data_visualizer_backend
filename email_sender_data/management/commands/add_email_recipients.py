from django.db import transaction
from email_sender.models import RecipientGroup, Recipient

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args, **options):
        recipients = [
            {
                "email": "mcdancher18@gmail.com",
                "groups": [1, 2],
            },
            {
                "email": "dancher072@gmail.com",
                "groups": [3],
            },
            {
                "email": "mike@trounceflow.com",
                "groups": [1, 2],
            },          
            {
                "email": "trounceflow@gmail.com",
                "groups": [2, 3],
            },
            {
                "email": "michael.trounce@exantedata.com",
                "groups": [2, 3],
            }
        ]
        for recipient in recipients:
            groups = []
            for group_number in recipient['groups']:
                groups.append(RecipientGroup.objects.get_or_create(name=f"Group_{group_number}")[0])
            recipient = Recipient.objects.create(email=recipient['email'])
            recipient.groups.add(*groups)
