from django.urls import include, path
from api.comment.views import CommentCreateView, CommentRetrieveUpdateDestroyView

urlpatterns = [
    path("", CommentCreateView.as_view()),
    path(
        "<uuid:uuid>/",  # first one is type of field : second one is field name
        CommentRetrieveUpdateDestroyView.as_view(
            lookup_field="uuid",  # tell it, i'm querying with uuid
        ),
    ),
    path(
        "<int:pk>/",  # first one is type of field : second one is field name - if int:pk, no need for the lookup field
        CommentRetrieveUpdateDestroyView.as_view(
            # lookup_field="id",  # tell it, i'm querying with id
        ),
    ),
]
