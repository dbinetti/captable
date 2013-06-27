import requests

from .models import MobileUser

from .utils import sendcode

class NoncenseBackend(object):
    """Nonce over SMS authentication backend.

    This backend uses a simplified four-digit nonce sent over
    SMS to authenticate users.
    """

    def authenticate(self, mobile=None):
        """Authenticate over nonce service

        Authenticates if the user passes against a nonce service.
        """
        nonce_user = NonceUser(mobile)
        if nonce_user.is_authenticated():
            try:
                user = MobileUser.objects.get(mobile=mobile)
            except MobileUser.DoesNotExist:
                user = MobileUser(mobile=mobile)
                user.save()
            return user


    def get_user(self, user_id):
        try:
            return MobileUser.objects.get(pk=user_id)
        except MobileUser.DoesNotExist:
            return None
