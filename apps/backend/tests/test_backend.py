from unittest import mock

from django.test import TestCase
from django.conf import settings

from backend.tests.mixins import InterceptStdoutMixin
import backend.signals


class TestBackend(InterceptStdoutMixin, TestCase):
    @mock.patch('backend.signals.backend_called.send_robust')
    def test_backend_creation_signal(self, signal_mock):
        """ Test outgoing signal. """
        self.assertFalse(signal_mock.called)
        self._intercept_command_stdout('backend', run_once=True)
        self.assertTrue(signal_mock.called)

    @mock.patch('dsmr_backup.services.backup.check')
    @mock.patch('dsmr_backup.services.backup.sync')
    @mock.patch('dsmr_consumption.services.compact_all')
    @mock.patch('dsmr_mindergas.services.export')
    @mock.patch('dsmr_notification.services.notify')
    @mock.patch('dsmr_stats.services.analyze')
    @mock.patch('dsmr_weather.services.read_weather')
    def test_backend_creation_signal_receivers(self, *mocks):
        """ Test whether outgoing signal is received. """
        for current in mocks:
            self.assertFalse(current.called)

        self._intercept_command_stdout('backend', run_once=True)

        for current in mocks:
            self.assertTrue(current.called)

    def test_robust_signal(self):
        """ Test whether the signal is robust, handling any exceptions. """

        def _fake_signal_troublemaker(*args, **kwargs):
            raise BrokenPipeError("Signal receiver crashed for some reason...")

        backend.signals.backend_called.connect(receiver=_fake_signal_troublemaker)

        # We must disconnect to prevent other tests from failing, since this is no database action.
        backend.signals.backend_called.disconnect(receiver=_fake_signal_troublemaker)

    @mock.patch('traceback.format_tb')
    def test_signal_exception_handling(self, format_tb_mock):
        """ Tests signal exception handling. """
        def _fake_signal_troublemaker(*args, **kwargs):
            raise AssertionError("Crash")

        backend.signals.backend_called.connect(receiver=_fake_signal_troublemaker)
        self.assertFalse(format_tb_mock.called)

        self._intercept_command_stdout('backend', run_once=True)
        self.assertTrue(format_tb_mock.called)

    def test_supported_vendors(self):
        """ Check whether supported vendors is as expected. """
        self.assertEqual(
            settings.DSMRREADER_SUPPORTED_DB_VENDORS,
            ('postgresql', 'mysql')
        )

    def test_timezone(self):
        """ Verify timezone setting, as it should never be altered. """
        self.assertEqual(settings.TIME_ZONE, 'Europe/Amsterdam')

    def test_version(self):
        """ Verify version setting. """
        self.assertIsNotNone(settings.DSMRREADER_VERSION)

    def test_pending_migrations(self):
        """ Tests whether there are any model changes, which are not reflected in migrations. """
        self.assertEqual(
            self._intercept_command_stdout('makemigrations', dry_run=True),
            'No changes detected\n',
            'Pending model changes found, missing in migrations!'
        )

    def test_internal_check(self):
        """ Tests whether Django passes it's internal 'check' command. """
        self.assertEqual(
            self._intercept_command_stdout('check'),
            'System check identified no issues (0 silenced).\n',
        )
