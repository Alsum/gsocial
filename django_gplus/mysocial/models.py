from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
# Create your models here.

class EmailConfirmed(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    activation_key = models.CharField(max_length=200)
    confirmed = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.confirmed)

    def activate_user_email(self):
        # send email here & render a string
        activation_url = "%s%s" % (settings.SITE_URL, reverse("mysocial:activation_view", args=[self.activation_key]))
        context = {
            "activation_key": self.activation_key,
            "activation_url": activation_url,
            "user": self.user.username,
        }
        message = render_to_string("registration/activation_message.txt", context)
        subject = "Activate your Email"
        self.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.user.email], kwargs)
