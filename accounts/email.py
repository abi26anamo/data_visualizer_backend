from django.contrib.auth.tokens import default_token_generator
from templated_mail.mail import BaseEmailMessage

from djoser import utils
from djoser.conf import settings

# Define custom email classes for various user actions.


class ActivationEmail(BaseEmailMessage):
    """
    Email class for sending activation links to users upon registration.
    Inherits from BaseEmailMessage.
    """
    template_name = "accounts/email/activation.html"

    def get_context_data(self):
        """
        Generates context data for the activation email template.
        Returns a dictionary containing necessary data for email rendering.
        """
        context = super().get_context_data()

        user = context.get("user")
        # Encodes user primary key for security
        context["uid"] = utils.encode_uid(user.pk)
        # Generates a token for user activation
        context["token"] = default_token_generator.make_token(user)
        # Constructs the activation URL using settings
        context["url"] = settings.ACTIVATION_URL.format(**context)
        context["domain"] = settings.DOMAIN
        context['protocol'] = 'https'  # Add your desired protocol here
        context['site_name'] = 'Exante Data'  # Add your site name here

        return context


class ConfirmationEmail(BaseEmailMessage):
    """
    Generic confirmation email template class.
    Inherits from BaseEmailMessage.
    """
    template_name = "accounts/email/confirmation.html"


class PasswordResetEmail(BaseEmailMessage):
    """
    Email class for sending password reset links to users.
    Inherits from BaseEmailMessage.
    """
    template_name = "email/password_reset.html"

    def get_context_data(self):
        """
        Generates context data for the password reset email template.
        Returns a dictionary containing necessary data for email rendering.
        """
        context = super().get_context_data()

        user = context.get("user")
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        # Constructs the password reset URL using settings
        context["url"] = settings.PASSWORD_RESET_CONFIRM_URL.format(**context)
        context["domain"] = settings.DOMAIN
        context['protocol'] = 'https'  # Add your desired protocol here
        context['site_name'] = 'Exante Data'

        return context


class PasswordChangedConfirmationEmail(BaseEmailMessage):
    """
    Email class for notifying users about successful password change.
    Inherits from BaseEmailMessage.
    """
    template_name = "accounts/email/password_changed_confirmation.html"


class UsernameChangedConfirmationEmail(BaseEmailMessage):
    """
    Email class for notifying users about successful username change.
    Inherits from BaseEmailMessage.
    """
    template_name = "accounts/email/username_changed_confirmation.html"


class UsernameResetEmail(BaseEmailMessage):
    """
    Email class for sending username reset links to users.
    Inherits from BaseEmailMessage.
    """
    template_name = "accounts/email/username_reset.html"

    def get_context_data(self):
        """
        Generates context data for the username reset email template.
        Returns a dictionary containing necessary data for email rendering.
        """
        context = super().get_context_data()

        user = context.get("user")
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        # Constructs the username reset URL using settings.
        context["url"] = settings.USERNAME_RESET_CONFIRM_URL.format(**context)
        context["domain"] = settings.DOMAIN
        context['protocol'] = 'https'
        context['site_name'] = 'Exante Data'
        return context
