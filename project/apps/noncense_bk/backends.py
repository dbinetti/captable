from .models import MobileUser


class PhoneBackend(object):
    """
    Simplified backend that assumes an empheral, session-based authentication
    such that persistent passwords are not required.
    Note that calling this method will *always* return an authenticated user.
    """

    def authenticate(self, mobile):
        user, created = MobileUser.objects.get_or_create(mobile=mobile)
        return user

    def get_user(self, user_id):
        try:
            return MobileUser.objects.get(pk=user_id)
        except MobileUser.DoesNotExist:
            return None
