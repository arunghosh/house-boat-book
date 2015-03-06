from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from phonenumber_field.modelfields import PhoneNumber


class UserManager(BaseUserManager):
    UT_UNKNOWN = 0
    UT_CUSTOMER = 1
    UT_AGENT = 2
    UT_OWNER = 3
    UT_BOK = 4

    USER_TYPES = (
        (UT_UNKNOWN, "Unknown"),
        (UT_AGENT, "Agent"),
        (UT_BOK, "Boats ok Kerala"),
        (UT_CUSTOMER, "Customer"),
        (UT_OWNER, "Owner"),
    )

    def create_user(self, email, u_type=UT_UNKNOWN, phone=None, name=None, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=UserManager.normalize_email(email),
            name=name,
            phone=phone,
            type=u_type)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_customer(self, email, phone, name):
        user = self.create_user(email,
                                name=name,
                                u_type=UserManager.UT_CUSTOMER,
                                phone=phone)
        return user

    def create_owner(self, email, phone, name):
        user = self.create_user(email,
                                name=name,
                                u_type=UserManager.UT_OWNER,
                                phone=phone)
        return user

    def create_superuser(self, email, password, name):
        user = self.create_user(email,
                                name=name,
                                u_type=UserManager.UT_BOK,
                                password=password,)
        user.is_admin = True
        user.save(using=self._db)
        return user


class BaseUser(AbstractBaseUser):

    email = models.EmailField(max_length=254, unique=True, db_index=True)
    phone = models.CharField(max_length=16, blank=True, null=True)
    name = models.CharField(max_length=128)
    type = models.PositiveSmallIntegerField(choices=UserManager.USER_TYPES, default=UserManager.UT_UNKNOWN)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    @property
    def type_str(self):
        return [b for (a, b) in UserManager.USER_TYPES if a == self.type][0]

    @property
    def is_customer(self):
        return self.type == UserManager.UT_CUSTOMER

    @property
    def is_owner(self):
        return self.type == UserManager.UT_OWNER

    @property
    def is_bok(self):
        return self.type == UserManager.UT_BOK or self.is_admin


    def get_full_name(self):
        # For this case we return email. Could also be User.first_name User.last_name if you have these fields
        return self.email

    def get_short_name(self):
        # For this case we return email. Could also be User.first_name if you have this field
        return self.email

    def __unicode__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        # Handle whether the user has a specific permission?"
        return True

    def has_module_perms(self, app_label):
        # Handle whether the user has permissions to view the app `app_label`?"
        return True

    @property
    def is_staff(self):
        # Handle whether the user is a member of staff?"
        return self.is_admin


# @receiver(post_save, sender=get_user_model())
# def create_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)