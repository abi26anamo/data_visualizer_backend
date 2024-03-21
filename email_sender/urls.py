from django.urls import path

from .views import (
    SendEmailAPIView, RecipientGroupView, RecipientView,
    # LetterTemplateView, GetEmailGroupView, SendEmailGroupView,
)


urlpatterns = [
    path("recipient-groups/", RecipientGroupView.as_view(), name="recipient-groups"),
    path("recipients/", RecipientView.as_view(), name="recipients"),

    path("send-email/", SendEmailAPIView.as_view(), name="index"),

    # path("send-email-group/", SendEmailGroupView.as_view(), name="send-email-group"),
    # path("email-templates/", LetterTemplateView.as_view(), name="email-templates"),
]
