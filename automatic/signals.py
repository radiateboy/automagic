from django.dispatch import Signal

USER_REGISTERED_SIGNAL = Signal(providing_args=['user'])