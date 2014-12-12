from rest_framework import generics

from .mixins import SearchMixin

class SearchAPIView(SearchMixin, generics.ListAPIView):
    pass
