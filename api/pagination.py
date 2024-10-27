# for pagination 2
from django.conf import settings
from rest_framework import pagination
from rest_framework.response import Response


class PageNumberPagination(pagination.PageNumberPagination):
    last_page_strings = [
        "last",  # By default, when a client requests the last page of results in DRF, it uses the word "last" in the URL to represent the last page.
    ]
    max_page_size = settings.API_MAX_PAGE_SIZE  # max size per page
    page_query_param = "page"  # page param: e.g `page`=1
    page_size = (
        settings.API_DEFAULT_PAGE_SIZE  # default page size: count of object in the page
    )
    page_size_query_param = "limit"  # page size argument `limit`=1

    #  override the response returned by paginating
    def get_paginated_response(self, data):
        return Response(
            {
                "count": self.page.paginator.count,  # number of items on the page
                "page": self.page.number,
                "num_pages": self.page.paginator.num_pages,
                "limit": self.page.paginator.per_page,  # max items in a page
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
            }
        )
