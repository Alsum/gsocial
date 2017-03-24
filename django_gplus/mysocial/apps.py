from __future__ import unicode_literals

from django.apps import AppConfig


class MysocialConfig(AppConfig):
    name = 'mysocial'
    def ready(self):
        import signals