# Optional : allows the ability for a request to be filtered by certain parameters
from content.models import Post
from django_filters import FilterSet, NumberFilter


#  create a post filter and inherit from Filterset
class PostFilter(FilterSet):
    # allow for posts to be filtered by owner - expects that client will query with user id
    owner = NumberFilter(
        field_name="owner",  # look up
    )

    class Meta:
        model = Post  # what model is being used by the filter
        fields = ["owner"]  # the fields being used
