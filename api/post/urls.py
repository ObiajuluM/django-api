from cgitb import lookup
from django.urls import include, path
from .views import PostListCreateView, PostRetrieveUpdateDestroyView

urlpatterns = [
    path("", PostListCreateView.as_view()),
    path(
        "<uuid:uuid>/",  # first one is type of field : second one is field name
        PostRetrieveUpdateDestroyView.as_view(
            lookup_field="uuid",  # tell it, i'm querying with uuid
        ),
    ),
    path(
        "<int:id>/",  # first one is type of field : second one is field name - if int:pk, no need for the lookup field
        PostRetrieveUpdateDestroyView.as_view(
            lookup_field="id",  # tell it, i'm querying with uuid
        ),
    ),
]
