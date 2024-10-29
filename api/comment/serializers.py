from email.policy import default
from typing import Required
from rest_framework import serializers
from content.models import Comment
from api.user.serializers import UserPublicSerializer
from api.post.querysets import PUBLIC_POSTS_QUERYSET


class CommentSerializer(serializers.ModelSerializer):

    owner = UserPublicSerializer(read_only=True)

    class Meta:
        model = Comment  # the model we are serializing

        # fields the serializer is supposed to return
        fields = [
            "uuid",
            "owner",
            "body",
            "created_at",
        ]

        # set readonly fields, because the serializer will also be used for creating posts
        # you dont want the user to send up or edit any of the below fields
        read_only = [
            "uuid",
            "owner",
            # "owner",
            "created_at",
        ]


class CommentCreateSerializer(serializers.Serializer):

    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),  # use the current user as param [via user]
    )

    #  this returns the post itself not the uuid
    post = serializers.SlugRelatedField(
        slug_field="uuid", queryset=PUBLIC_POSTS_QUERYSET  # filter by posts
    )

    body = serializers.CharField()
