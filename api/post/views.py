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
from content.models import Post
from .querysets import ALL_POSTS_QUERYSET, PUBLIC_POSTS_QUERYSET
from .serializers import PostSerializer
from .filters import PostFilter

# region: python thing for organizing code


# region Base Classes
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


class PostMeApiView(PostApiView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # return all posts the user created that isnt marked as deleted
        return ALL_POSTS_QUERYSET.filter(owner=self.request.user)


# endregion


# region Public


#  create endpoint for creating a post and listing a posts
class PostListCreateView(
    ListModelMixin,
    CreateModelMixin,
    PostApiView,
):

    # authenticated unless error
    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

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


class PostRetrieveView(
    RetrieveModelMixin,
    PostApiView,
):
    # get request a single item in the db
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


# endregion


# region Me
class PostMeListView(ListModelMixin, PostMeApiView):

    # # set permission class
    # permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     # return all posts the user created that isnt marked as deleted
    #     return ALL_POSTS_QUERYSET.filter(owner=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


# endregion


class PostMeRetrieveUpdateDestroyView(
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    PostApiView,
):
    # get request a single item in the db
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    # put/update request a single item in the db - done for chnaging the whole data
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    # update /partial update request a single item in the db - changing aspects of the whole data ✅
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    # delete request a single item in the db
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    #  doing this to mark post as deleted by overriding the normal perform destroy - not actually delete
    def perform_destroy(self, instance: Post):
        instance.status = Post.Status.REMOVED
        instance.save()
        # return super().perform_destroy(instance)
