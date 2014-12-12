from rest_framework import serializers
from rest_framework.fields import *

from haystack import indexes

from .fields import *

class SearchIndexSerializerOptions(serializers.SerializerOptions):
    """
    Meta class options for SearchIndexSerializer
    """
    def __init__(self, meta):
        super(SearchIndexSerializerOptions, self).__init__(meta)
        self.index = getattr(meta, 'index', None)

class SearchIndexSerializer(serializers.Serializer):
    _options_class = SearchIndexSerializerOptions

    pk = Field()

    field_mapping = {
        indexes.BooleanField: BooleanField,
        indexes.CharField: CharField,
        indexes.DateField: DateField,
        indexes.DateTimeField: DateTimeField,
        indexes.DecimalField: DecimalField,
        indexes.EdgeNgramField: CharField,
        indexes.FloatField: FloatField,
        indexes.IntegerField: IntegerField,
        #indexes.LocationField: None,
        #indexes.MultivalueField: None,
        indexes.NgramField: CharField,

        indexes.FacetBooleanField: BooleanField,
        indexes.FacetCharField: CharField,
        indexes.FacetDateField: DateField,
        indexes.FacetDateTimeField: DateTimeField,
        indexes.FacetDecimalField: DecimalField,
        indexes.FacetFloatField: FloatField,
        indexes.FacetIntegerField: IntegerField,
        #indexes.FacetMultivalueField: None,
    }

    def get_default_fields(self):
        """
        Return all the fields that should be serialized for the search index.
        """
        
        cls = self.opts.index
        assert cls is not None, (
            "Serializer class '%s' is missing 'index' Meta option" %
            self.__class__.__name__
        )

        ret = SortedDict()

        # Deal the primary key field
        ret['pk'] = serializers.Field()

        for f in cls.fields:
            ret[f] = self.get_field_from_index(cls.fields[f])

        return ret

    def get_field_from_index(self, index_field):
        kwargs = {
        }

        serializer_field_class = serializers._get_class_mapping(
            self.field_mapping, index_field)

        if serializer_field_class:
            return serializer_field_class(**kwargs)
        return Field(**kwargs)

class SearchSerializerOptions(serializers.SerializerOptions):
    """
    Meta class options for SearchSerializer
    """

class SearchSerializer(SearchIndexSerializer):
    _options_class = SearchSerializerOptions

    def get_default_fields(self):
        ret = SortedDict()

        # Deal the primary key field
        ret['pk'] = serializers.Field()
        
        return ret

    def to_native(self, obj):
        """
        Serialize objects -> primitives.
        """
        ret = self._dict_class()
        ret.fields = self._dict_class()
        
        # copypasta from
        # rest_framework.serializers.Serializer.to_native
        # goes here:
        for field_name, _field in obj.searchindex.fields.items():
            field = self.get_field_from_index(_field)
            field.initialize(parent=self, field_name=field_name)
            key = self.get_field_key(field_name)
            value = field.field_to_native(obj, field_name)
            method = getattr(self, 'transform_%s' % field_name, None)
            if callable(method):
                value = method(obj, value)
            if not getattr(field, 'write_only', False):
                ret[key] = value
            ret.fields[key] = self.augment_field(field, field_name, key, value)

        for field_name, field in self.fields.items():
            if field.read_only and obj is None:
                continue
            field.initialize(parent=self, field_name=field_name)
            key = self.get_field_key(field_name)
            value = field.field_to_native(obj, field_name)
            method = getattr(self, 'transform_%s' % field_name, None)
            if callable(method):
                value = method(obj, value)
            if not getattr(field, 'write_only', False):
                ret[key] = value
            ret.fields[key] = self.augment_field(field, field_name, key, value)

        return ret
