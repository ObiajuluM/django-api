from django.urls import include, path

urlpatterns = [
    path("auth/", include("api.auth.urls")),  # go api/auth/urls
    path("post/", include("api.post.urls")),  # go api/posts/urls
    path("comment/", include("api.comment.urls")),  # go to api/comments/urls
]
