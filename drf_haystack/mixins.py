from django.core import validators

from rest_framework import generics

from haystack.query import SearchQuerySet
from haystack.utils import Highlighter

from .serializers import SearchSerializer

class SearchMixin(object):
    queryset = SearchQuerySet()

    serializer_class = SearchSerializer

    highlighter_class = Highlighter # set to None for no highligthing

    search_parameter = 'q'
    
    load_all = False

    def get_highlighter(self, query):
        if self.highlighter_class:
            return self.highlighter_class(query)
        else:
            return None

    def get_query(self):
        try:
            query = self.query
        except:
            query = self.request.GET.get(self.search_parameter, '')
            query = query.strip()
            if query in validators.EMPTY_VALUES:
                query = ''
            self.query = query
        return query

    def get_serializer_context(self):
        context = super(SearchMixin, self).get_serializer_context()
        highlighter = self.get_highlighter(self.get_query())
        if highlighter:
            context['highlighter'] = highlighter
        return context

    def get_empty_queryset(self, qs): # if query is empty
        return qs.none()

    def get_queryset(self):
        qs = self.queryset
        query = self.get_query()
        if query == '':
            return self.get_empty_queryset(qs)
        else:
            qs = qs.filter(text=query)
            if self.load_all:
                return qs.load_all()
            else:
                return qs
