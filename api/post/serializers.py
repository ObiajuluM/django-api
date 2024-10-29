from rest_framework import serializers
from content.models import Post
from api.user.serializers import UserPublicSerializer


#  serialize the post object to json
class PostSerializer(serializers.ModelSerializer):

    # define the owner of the post
    owner = UserPublicSerializer(read_only=True)

    class Meta:
        model = Post  # the model we are serializing

        # fields the serializer is supposed to return
        fields = [
            "id",
            "uuid",
            "title",
            "owner",
            "body",
            "status",
            "created_at",
        ]

        # set readonly fields, because the serializer will also be used for creating posts
        # you dont want the user to send up or edit any of the below fields
        read_only = [
            "id",
            "uuid",
            "owner",
            # "owner",
            "created_at",
        ]
