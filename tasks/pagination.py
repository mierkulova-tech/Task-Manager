from rest_framework.pagination import PageNumberPagination
from rest_framework.pagination import CursorPagination


class SubTaskPagination(PageNumberPagination):
    page_size = 5


class SecureCursorPagination(CursorPagination):
    page_size = 6
    ordering = '-created_at'