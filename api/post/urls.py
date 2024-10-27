from cgitb import lookup
from django.urls import include, path
from .views import (
    PostListCreateView,
    PostMeListView,
    PostRetrieveView,
    PostMeRetrieveUpdateDestroyView,
)

urlpatterns = [
    path("", PostListCreateView.as_view()),
    path("me/", PostMeListView.as_view()),
    path(
        "<uuid:uuid>/",  # first one is type of field : second one is field name
        PostRetrieveView.as_view(
            lookup_field="uuid",  # tell it, i'm querying with uuid
        ),
    ),
    path(
        "<int:pk>/",  # first one is type of field : second one is field name - if int:pk, no need for the lookup field
        PostRetrieveView.as_view(
            # lookup_field="id",  # tell it, i'm querying with id
        ),
    ),
    path(
        "me/<uuid:uuid>/",  # first one is type of field : second one is field name
        PostMeRetrieveUpdateDestroyView.as_view(
            lookup_field="uuid",
        ),
    ),
    path(
        "me/<int:pk>/",  # first one is type of field : second one is field name - if int:pk, no need for the lookup field
        PostMeRetrieveUpdateDestroyView.as_view(),
    ),
]
