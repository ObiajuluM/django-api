# QuerySets makes it easier to get the data you actually need,
# by allowing you to filter and order the data at an early stage.

from content.models import Post


# get all the items in the db - without the ones marked as removed
ALL_POSTS_QUERYSET = Post.objects.all().exclude(status=Post.Status.REMOVED)

# all posts query set filtered by the ones marked as published
PUBLIC_POSTS_QUERYSET = Post.objects.filter(status=Post.Status.PUBLISHED)
