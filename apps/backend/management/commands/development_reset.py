from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.conf import settings


from mqtt.models.settings.broker import MQTTBrokerSettings
from mqtt.models import queue


class Command(BaseCommand):
    help = _('Resets the environment for development purposes. Not intended for production.')

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument(
            '--no-api',
            action='store_true',
            dest='no_api',
            default=False,
            help=_('Whether the API should be disabled.')
        )

    def handle(self, **options):
        if not settings.DEBUG:
            raise CommandError(_('Intended usage is NOT production! Only allowed when DEBUG = True'))

        MQTTBrokerSettings.objects.update(
            port=8883, secure=MQTTBrokerSettings.SECURE_CERT_NONE, debug=True, username='user', password='password'
        )
        queue.Message.objects.all().delete()


        try:
            # Reset passwd.
            admin = User.objects.get(username='admin')
        except User.DoesNotExist:
            User.objects.create_superuser('admin', 'root@localhost', 'admin')
        else:
            admin.set_password('admin')
            admin.save()
