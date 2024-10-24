from django.urls import include, path

urlpatterns = [
    path("post/", include("api.post.urls")),  # go api/posts/urls
    # path("comments/", include("api.comment.urls")),
]
