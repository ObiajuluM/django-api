import uuid
from click import edit
from django.db import models

# translation support in different languages
from django.utils.translation import gettext_lazy as _

# Create your models here.


# base models other models will inherit
class AbstractModel(models.Model):
    # generate a unique identifier everytime the model is made
    uuid = models.UUIDField(
        _("UUID"),  # name of the field with transaltion support
        default=uuid.uuid4(),  # default field for the uuid
        unique=True,  # make unique
        editable=False,  #  make not editable
        db_index=True,  # set to be used as db index - query by uuid
    )

    #
    created_at = models.DateTimeField(
        _("Created At"),  # field name + support translation
        auto_now_add=True,  # set datetime.now() when a new instance of the model is made
    )

    updated_at = models.DateTimeField(
        _("Updated At"),
        auto_now=True,  # anytime the instance of the model changes - update
    )

    class Meta:
        # this means this model will not create a database table - it there for other models to inherit
        abstract = True
        # set to sort the models in the databse by the newest first
        ordering = ["-created_at"]
