from django.dispatch import Signal


# Triggered whenever a 'backend' management command was called.
backend_called = Signal(providing_args=[])
