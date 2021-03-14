from rest_framework.pagination import LimitOffsetPagination


class CustomLimitOffsetPagination(LimitOffsetPagination):
    """
    Default pagination limit used to make all response return paginated even if no limit was set
    """
    default_limit = 10
