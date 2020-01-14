# -*- coding: utf-8 -*-

import datetime
import secrets

from django.db import models
from django.conf import settings
from django.contrib.auth.models import BaseUserManager, AbstractUser

class UserActivationKey(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    activation_key = models.CharField(max_length=64, null=True, blank=True)
    key_expires = models.DateTimeField(null=True, blank=True)

    @classmethod
    def set_random_key_for_user(cls, user, force=False):
        activation_key = secrets.token_hex()

        # Create and save their profile
        user_activation_key, created = cls.objects.get_or_create(user=user)
        if created or force:
            user_activation_key.activation_key = activation_key
            user_activation_key.key_expires = datetime.datetime.today() + datetime.timedelta(7)
            user_activation_key.save()

        return user_activation_key


class MyUserManager(BaseUserManager):
    # def current_time(self):
    #     """get current time """
    #     from datetime import datetime
    #     return datetime.now().strftime("%Y-%m-%d")

    def create_user(self, username, email, password):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """

        if not username:
            raise ValueError('username is unique')
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        """
        Creates and saves a superuser with the given email, password.
        """
        user = self.create_user(username, email, password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    Dept_Choice = (
        ('测试', '测试'),
        ('开发', '开发'),
    )
    realname = models.CharField(max_length=50, verbose_name="真实姓名", null=True, blank=True, editable=True)
    mobile = models.CharField(max_length=11, verbose_name="电话号码", null=True, blank=True, editable=True)
    email = models.EmailField(verbose_name='邮箱', max_length=255, unique=True)
    dept = models.CharField(verbose_name=u'部门', choices=Dept_Choice, default='测试', max_length=100)
    is_active = models.BooleanField(default=True, verbose_name='激活状态')
    is_admin = models.BooleanField(default=False, verbose_name='是否管理员')
    testrailuser = models.CharField(max_length=50, verbose_name="TestRail用户名", null=True, blank=True, editable=True)
    testrailpass = models.CharField(max_length=50, verbose_name="TestRail密码", null=True, blank=True, editable=True)
    def get_full_name(self):
        # The user is identified by their email address
        return self.username

    def get_short_name(self):
        # The user is identified by their email address
        return self.username

    def __unicode__(self):  # __unicode__ on Python 2
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True