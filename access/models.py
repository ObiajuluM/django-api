from django.db import models
from django.utils.translation import gettext_lazy as _
from common.models import AbstractModel
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.


#  create custom user manager
class UserManager(BaseUserManager):
    #  override from stuff ⬇️ that django needs

    # internal function
    def _create_user(self, password, **kwargs):
        # access to the model
        user = self.model(**kwargs)
        #  define password : we will salt and hash - to validate login
        user.set_password(password)
        # save the user : using self.db
        user.save(using=self.db)
        return user

    #  normal create user function : that will be called
    def create_user(self, password, **kwargs):
        #  set admin right to false
        kwargs["is_admin"] = False
        return self._create_user(password, **kwargs)

    # that command that ran that year -  to create an admin
    # we overrode so it won't expect a username
    def create_superuser(self, password, **kwargs):
        kwargs["is_admin"] = True
        return self._create_user(password, **kwargs)


# """this is a custom model - doesnt directly inherit from django's models.Model"""
# user inherits from the base abstract model and django's abstract base user
class User(AbstractModel, AbstractBaseUser):

    email = models.EmailField(
        _("Email"),
        max_length=128,
        # blank=True,
        # null=True, # allow to be null
        unique=True,
        db_index=True,
    )

    name = models.CharField(
        _("Name"),
        max_length=32,
        blank=True,  # allow to be empty
    )

    password = models.CharField(
        _("Password"),
        max_length=128,
    )

    # activate or deactivate account
    is_active = models.BooleanField(
        _("Active"),
        help_text=("Designates whether this user can access their account."),
        default=True,
    )

    is_admin = models.BooleanField(
        _("Admin"),
        help_text=("Designates whether this user can log into the admin site."),
        default=False,
    )

    # string representation of the model
    def __str__(self) -> str:
        return self.name + self.email

    """ Django required  beacuse we inherited from the AbstractBaseUser ⬇️"""
    # tell django to use email as the user name field - beacuse we inherited from the AbstractBaseUser
    USERNAME_FIELD = "email"

    # override the base manager of the model
    objects = UserManager()

    #  create properties - methods that can be called without parenthesis to return properties - like a dart getter
    @property
    def is_staff(self):
        """they are staff if admin"""
        return self.is_admin

    @property
    def is_superuser(self):
        """they are superusers if admin"""
        return self.is_admin

    #  if user has permission : if they are active and are admin
    def has_perm(self, perm, obj=None):
        return self.is_active and self.is_admin

    #  if user has modular permission
    def has_module_perms(self, app_label):
        return self.is_active and self.is_admin

    #
    def get_all_permissions(self, obj=None):
        return []

    # make meta class and inherit from the base Abstract model
    class Meta(AbstractModel.Meta):
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    # override the base manager of the model
    # objects = BaseUserManager()
