from rest_framework import serializers
from content.models import Post


#  serialize the post object to json
class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post  # the model we are serializing

        # fields the serializer is supposed to return
        fields = [
            "id",
            "uuid",
            "title",
            "body",
            "created_at",
        ]

        # set readonly fields, because the serializer will also be used for creating posts
        # you dont want the user to send up or edit any of the below fields
        read_only = [
            "id",
            "uuid",
            "owner",
            "created_at",
        ]
