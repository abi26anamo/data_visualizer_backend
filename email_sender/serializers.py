from rest_framework import serializers
from .models import RecipientGroup, Recipient


class RecipientGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipientGroup
        fields = ["id", "name"]


class RecipientSerializer(serializers.ModelSerializer):
    groups = RecipientGroupSerializer(many=True)

    class Meta:
        model = Recipient
        fields = ["id", "email", "groups"]


class EmailSerializer(serializers.Serializer):
    """
    Serializer for email data that validates data necessary to send an email.
    Such subject, body, and attachments.

    Fields:
    - subject (CharField): The subject line of the email, which cannot exceed 200 characters.
    - html_content (CharField): The HTML content that will make up the body of the email.
    - attachments (ListField): An optional field allowing a list of file attachments.
        Each file is represented and validated by a FileField.
    """

    subject = serializers.CharField(max_length=200)
    html_content = serializers.CharField()
    attachments = serializers.ListField(
        child=serializers.FileField(),
        required=False
    )


# class LetterTemplateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = LetterTemplate
#         fields = ["id", "title", "content", "updated", "type"]
#         read_only_fields = ['id', 'updated']

