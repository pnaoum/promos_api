from rest_framework.pagination import LimitOffsetPagination


class CustomLimitOffsetPagination(LimitOffsetPagination):
    """
    Default pagination limit added to make all responses paginated even if no limit was set for consistency
    """
    default_limit = 10
