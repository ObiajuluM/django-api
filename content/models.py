from django.db import models
from django.utils.translation import gettext_lazy as _
from common.models import AbstractModel
from access.models import User

# Create your models here.


class Post(AbstractModel):

    #  define owner - all posts will be related to a user
    owner = models.ForeignKey(
        User,  # the model that will be related to this foreign key
        verbose_name=_("Owner"),  # presentation name
        related_name="posts",  # for django relations and you can call `User.posts`
        # post exists with user1 but user1 gets deleted
        on_delete=models.CASCADE,  # if user is deleted, delete post. if field is nullable use SET_NULL: requires the owner field be optional else cascade
    )

    # post title
    title = models.CharField(
        _("Title"),
        max_length=255,
    )

    # post body
    #  text field for long form content
    body = models.TextField(_("Body"))

    # class to define the status of the post
    class Status(models.TextChoices):
        #  first item is how it is stored in the db - second is the presentation  of it in the admin
        DRAFT = "draft", _("Draft")
        PUBLISHED = "published", _("Published")
        REMOVED = "removed", _(
            "Removed"
        )  # stuff is marked as deleted -  but not deleted from db

    # post status - if post is published, removed, draft etc
    status = models.CharField(
        _("Status"),
        max_length=16,
        choices=Status.choices,  # validation to confirm the data passed is a property of the status class
        default=Status.DRAFT,  # by default they are all drafts
    )

    #  string representation in admin
    def __str__(self) -> str:
        return self.title


#  comment model
class Comment(AbstractModel):
    #  define owner - all comments will be related to a user
    owner = models.ForeignKey(
        User,  # the model that will be related to this foreign key
        verbose_name=_("Owner"),  # presentation name
        related_name="comments",  # for django relations and you can call `User.comments`
        on_delete=models.CASCADE,  # if user is deleted, delete comment. if field is nullable use SET_NULL: requires the owner field be optional else cascade
    )

    #  post the comment is tied to
    post = models.ForeignKey(
        Post,  # the model that will be related to this foreign key
        verbose_name=_("Post"),  # presentation name
        related_name="comments",  # for django relations and you can call `Post.comments`
        on_delete=models.CASCADE,
        
    )

    # body of the comment
    body = models.TextField(
        _("Body"),
    )

    #  if comment is deleted
    is_deleted = models.BooleanField(
        _("Is deleted"),
        default=False,
    )

    #  string representation in admin
    def __str__(self) -> str:
        return self.body
