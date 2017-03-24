import random
import hashlib
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from .models import EmailConfirmed



def user_created(sender, instance, created, *args, **kwargs):
    user = instance
    if created and not user.is_active:
        email_confirmed, email_is_created = EmailConfirmed.objects.get_or_create(user=user)
        if email_is_created:
            short_hash = hashlib.sha1(str(random.random())).hexdigest()[:5]
            base, domain = str(user.email).split("@")
            activation_key = hashlib.sha1(short_hash + base).hexdigest()
            email_confirmed.activation_key = activation_key
            email_confirmed.save()
            email_confirmed.activate_user_email()


post_save.connect(user_created, sender=User)
