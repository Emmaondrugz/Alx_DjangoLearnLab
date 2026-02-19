from rest_framework.pagination import PageNumberPagination

class StandardResultsPagination(PageNumberPagination):
    page_size = 10 # Number of times per page
    page_size_query_param = 'page_size' # Allow user to choose size (e.g. ?page_size=20)

