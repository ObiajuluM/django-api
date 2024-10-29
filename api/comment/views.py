from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.mixins import (
    # help us write less code for our api
    DestroyModelMixin,
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)

from api.permissions import AllowAny, IsAuthenticated, IsCommentOrPostOwner
from content.models import Comment
from .querysets import ALL_COMMENTS_QUERYSET
from .serializers import CommentCreateSerializer, CommentSerializer
from api.exceptions import BadRequest


# region base class


class CommentApiView(GenericAPIView):
    queryset = ALL_COMMENTS_QUERYSET
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]

    ordering_fields = ["created_at"]
    ordering = ["-created_at"]


# endregion


# region public


class CommentListView(ListModelMixin, CommentApiView):
    def get(self, request, *args, **kwargs):
        #  kwargs has all the paramters - the name of the field after the colon in the url
        if kwargs.get("uuid"):
            #  if the comment is looked up by uuid - change the query set
            self.queryset = ALL_COMMENTS_QUERYSET.filter(
                # look up for all posts where the uuid is equal to the uuid passed
                post__uuid=kwargs.get("uuid")
            )
        elif kwargs.get("pk"):
            #  if the comment is looked up by pk - change the query set
            self.queryset = ALL_COMMENTS_QUERYSET.filter(
                # look up for all posts where the pk is equal to the pk passed
                post__id=kwargs.get("pk")
            )
        else:
            #  exit function and send reponse to the api client
            raise BadRequest()
        return self.list(request, *args, **kwargs)


# endregion


# region authenticated
class CommentCreateView(CommentApiView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        owner = serializer.validated_data.get("owner")
        post = serializer.validated_data.get("post")
        body = serializer.validated_data.get("body")

        #  create the comment
        comment = Comment.objects.create(
            owner=owner,
            post=post,
            body=body,
        )

        return Response(
            data=CommentSerializer(comment).data,
            status=status.HTTP_201_CREATED,
        )


class CommentRetrieveUpdateDestroyView(
    RetrieveModelMixin,
    DestroyModelMixin,
    CommentApiView,
):

    # using this field forces all the requests in the class to abound by the permission(s) defined in it
    permission_classes = [AllowAny]

    #  use this to override permissions for some methods
    def get_permissions(self):
        if self.request.method == "DELETE":
            self.permission_classes = [IsCommentOrPostOwner]
        return super().get_permissions()  # let rest do its thing

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def perform_destroy(self, instance: Comment):
        instance.is_deleted = True
        instance.save()


# endregion
