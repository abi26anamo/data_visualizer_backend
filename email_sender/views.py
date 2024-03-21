
import re
import io
import uuid
import base64
import threading

import boto3
from bs4 import BeautifulSoup
from botocore.exceptions import NoCredentialsError

from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .helper import send_email
from .models import RecipientGroup, Recipient
from .serializers import RecipientGroupSerializer, RecipientSerializer, EmailSerializer


class RecipientGroupView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            recipient_groups = RecipientGroup.objects.all()
            serializer = RecipientGroupSerializer(recipient_groups, many=True)
            return Response(serializer.data)
        except RecipientGroup.DoesNotExist:
            return Response(
                {"error": "An error ocured while tring to retrive recipient groups"},
                status=status.HTTP_404_NOT_FOUND,
            )


class RecipientView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            recipients = Recipient.objects.all()
            serializer = RecipientSerializer(recipients, many=True)
            return Response(serializer.data)
        except RecipientGroup.DoesNotExist:
            return Response(
                {"error": "An error ocured while tring to retrive recipients"},
                status=status.HTTP_404_NOT_FOUND,
            )


class SendEmailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            if not (group_ids := request.query_params.get('groups', '')):
                return Response({"error": "No group IDs provided"}, status=status.HTTP_400_BAD_REQUEST)

            group_ids = [int(group_id) for group_id in group_ids.strip('[]').split(',')]

            recipients = Recipient.objects.filter(groups__id__in=group_ids).distinct('email')
            if not (recipient_emails := [recipient.email for recipient in recipients]):
                return Response({"error": "No user email founds"}, status=status.HTTP_400_BAD_REQUEST)

            serializer = EmailSerializer(data=request.data)
            if serializer.is_valid():
                data = serializer.validated_data
                subject = data["subject"]
                html_content = data["html_content"]

                attachments = data.get("attachments", [])
                s3 = boto3.client(
                    's3',
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                )
                bucket_name = settings.AWS_STORAGE_BUCKET_NAME
                folder_path = settings.AWS_STORAGE_FOLDER

                email_content = BeautifulSoup(html_content, "html.parser").prettify()

                attachment_files_urls = []
                for attachment in attachments:
                    try:
                        s3_key = f'{folder_path}{attachment.name}'
                        s3.upload_fileobj(attachment, bucket_name, s3_key)
                        file_url = f'https://{bucket_name}.s3.amazonaws.com/{s3_key}'
                        attachment_files_urls.append(file_url)
                    except NoCredentialsError:
                        return Response(
                            {
                                'status': 'error',
                                'message': 'AWS credentials not available.'
                            },
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR
                        )

            soup = BeautifulSoup(html_content, "html.parser")
            for img_tag in soup.find_all("img"):
                src = img_tag.get("src")
                if src.startswith("data:image"):
                    base64_data = re.sub("^data:image/.+;base64,", "", src)
                    try:
                        image_data = base64.b64decode(base64_data)
                        image_io = io.BytesIO(image_data)
                        unique_filename = str(uuid.uuid4())

                        s3_key = f"{folder_path}{unique_filename}.png"
                        s3.upload_fileobj(image_io, bucket_name, s3_key)

                        img_tag["src"] = f"https://{bucket_name}.s3.amazonaws.com/{s3_key}"
                        img_tag["style"] = "max-width: 100%;"  # TODO: remove this from backend and handle it on frontend
                    except Exception as e:
                        return Response(
                            {
                                "message": str(e),
                            },
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        )
            try:
                email_content = soup.prettify()
                send_email_thread = threading.Thread(
                    target=send_email,
                    args=(
                        recipient_emails,
                        subject,
                        email_content,
                        attachment_files_urls
                    )
                )
                send_email_thread.start()

                return Response({"message": "Emails sent successfully"}, status=status.HTTP_200_OK)
            except:
                return Response({"error": "Failed to send email"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class LetterTemplateView(APIView):
#     """
#     API view for managing email templates.

#     Methods:
#     - get: Retrieve all email templates or a specific template by ID.
#     - post: Create a new email template.
#     """
#     def get(self, request, id, format=None):
#         """
#         Retrieve all email templates or a specific template by ID.

#         Args:
#         - request: HTTP request object.
#         - id: Optional ID of the email template to retrieve.
#         - format: Optional format suffix.

#         Returns:
#         - Response: JSON response with email template data or error message.
#         """

#         try:
#             email_templates = LetterTemplate.objects.all()
#             serializer = LetterTemplateSerializer(email_templates)
#             return Response(serializer.data)
#         except LetterTemplate.DoesNotExist:
#             return Response(
#                 {"error": "An error ocured while tring to retrive email templates"},
#                 status=status.HTTP_404_NOT_FOUND,
#             )

#     def post(self, request, format=None):
#         """
#         Create a new email template.

#         Args:
#         - request: HTTP request object.
#         - format: Optional format suffix.

#         Returns:
#         - Response: JSON response with created email template data or error message.
#         """
#         serializer = LetterTemplateSerializer(data=request.data)
#         if serializer.is_valid():
#             # Save email templates instance
#             email_templates_instance = serializer.save()

#             return Response(email_templates_instance.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
