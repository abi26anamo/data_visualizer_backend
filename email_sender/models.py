from django.db import models
from django.db.models import Model, ManyToManyField


class RecipientGroup(Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Recipient Group"
        verbose_name_plural = "Recipient Groups"
        ordering = ["-name"]


class Recipient(Model):
    email = models.EmailField(max_length=255, unique=True, blank=False, null=False)
    groups = ManyToManyField(RecipientGroup)

    def __str__(self):
        return self.email

    class Meta:
        ordering = ["-email"]


# class SentLetter(Model):
#     created_at = models.DateTimeField(auto_now_add=True)
#     subject = models.CharField()


# class LetterTemplate(models.Model):
#     """
#     Model representing email templates.

#     Attributes:
#     - title: Title of the email template.
#     - content: Content of the email template.
#     - updated: Date and time when the email template was last updated.
#     - type: Type of the email template.
#     """
#     title = models.CharField(max_length=255, default="")
#     content = models.TextField()
#     updated = models.DateTimeField(auto_now=True)
#     type = models.CharField(max_length=255, default="")
