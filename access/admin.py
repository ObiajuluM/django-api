from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from access.models import User

# Register your models here.
#  register the user model to show up on the admin panel

# admin.site.register(User) # this should have been normal


#  register user model
@admin.register(User)
class UserAdmin(BaseUserAdmin):  #  create class [modelname]+admin
    #  configure stuff about admin

    # fields you wanted to be searched
    search_fields = ["email", "name"]

    # force readonly fields - make fields unchangeable*
    readonly_fields = [
        "id",
        "uuid",
        "created_at",
        "updated_at",
    ]

    # shows up on the list page in a table
    # make sure the first thing in the list display wont be blank - b/c this is what you have to click on
    list_display = [
        "email",
        "name",
        "is_active",
        "is_admin",
        "created_at",
    ]

    # filtering : filter by items
    list_filter = [
        "is_active",
        "is_admin",
        "created_at",
    ]

    # b/c we inherited from the `BaseUserAdmin` : set to empty b/c we don't have groups and user permissions
    filter_horizontal = []

    # add sort for date - something like that
    date_hierarchy = "created_at"

    #  order/sort/show up as latest first
    ordering = ["-created_at"]

    #  field sets are literally arranging attributes of your models into different fields
    # optional: used to create a new one from scratch
    add_fieldsets = (
        (
            _("Details"),
            {"fields": ["name", "email"]},
        ),
        (
            _("Access"),
            {"fields": ["is_active", "is_admin"]},
        ),
        # (
        #     _("Data"),
        #     {"fields": ["metadata"]},
        # ),
    )

    #  required: if add_fieldsets isnt available, django will use this - is default when editing
    fieldsets = (
        (
            _("Details"),
            {"fields": ["id", "uuid", "name", "email"]},
        ),
        (
            _("Access"),
            {"fields": ["is_active", "is_admin", "password"]},
        ),
        (
            _("Dates"),
            {"fields": ["created_at", "updated_at"]},
        ),
    )

    #  to prevent some weird things
    class Media:
        pass
