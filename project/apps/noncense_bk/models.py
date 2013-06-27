from django.db import models

from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser)


class MobileUserManager(BaseUserManager):
    def create_user(self, mobile, password=None):
        """
        Creates and saves a User with the given mobile number.
        Password is optional
        """
        if not mobile:
            raise ValueError('Users must have a mobile address')

        user = self.model(
            mobile=mobile,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile, password):
        """
        Creates and saves a superuser with the given mobile number
        and password.
        """
        user = self.create_user(
            mobile,
            password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class MobileUser(AbstractBaseUser):
    mobile = models.CharField(
        verbose_name='mobile phone',
        max_length=12,
        unique=True,
        db_index=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MobileUserManager()

    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        # The user is identified by their mobile phone
        return self.mobile

    def get_short_name(self):
        # The user is identified by their mobile phone
        return self.mobile

    def __unicode__(self):
        return self.mobile

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
