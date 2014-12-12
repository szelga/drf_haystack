from rest_framework import serializers

class HighlightField(serializers.CharField):
    def to_native(self, obj):
        try:
            return self.context['highlighter'].highlight(obj)
        except KeyError, e:
            return obj
