from django.http import HttpRequest
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    # help us write less code for our api
    DestroyModelMixin,
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)

from api.permissions import AllowAny, IsAuthenticated
from .querysets import ALL_POSTS_QUERYSET, PUBLIC_POSTS_QUERYSET
from .serializers import PostSerializer
from .filters import PostFilter


#  create default view for others to inherit from
class PostApiView(GenericAPIView):
    #  set the query set
    queryset = PUBLIC_POSTS_QUERYSET
    # define the serializer
    serializer_class = PostSerializer
    # set the filter
    filterset_class = PostFilter
    # set default permission class
    permission_classes = [AllowAny]

    # make API searchable
    search_fields = [
        "owner__name",  # search by owner - __ (double underscore) means the name property of the owner
        "title",  # search by title
    ]

    # stuff that could be orederable in the api - using the `ordering` param in a query
    ordering_fields = [
        "created_at",
    ]

    # default ordering
    ordering = ["-created_at"]


#  create endpoint for creating a post and listing a posts
class PostListCreateView(
    ListModelMixin,
    CreateModelMixin,
    PostApiView,
):

    # get request -  a list of the items in the db
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    # create request
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    # perform authentication on the incoming post request before
    def perform_create(self, serializer: PostSerializer):
        # to prevent the owner from being sent to the serializer in the post request (manually)
        serializer.save(
            owner=self.request.user,  # set owner as whatever user is making the create request
        )


class PostRetrieveUpdateDestroyView(
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    PostApiView,
):
    # get request a single item in the db
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class PostMeListView(ListModelMixin, PostApiView):

    # set permission class
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # return all posts the used created that isnt marked as deleted
        return ALL_POSTS_QUERYSET.filter(owner=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
