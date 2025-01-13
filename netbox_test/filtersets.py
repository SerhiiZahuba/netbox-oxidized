from netbox.filtersets import NetBoxModelFilterSet

from .models import TestNameServer, TestZone


class TestNameServerFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = TestNameServer
        fields = ('id', 'name')

    def search(self, queryset, name, value):
        return queryset.filter(name__icontains=value)

class TestZoneFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = TestZone
        fields = ('id', 'name')

    def search(self, queryset, name, value):
        return queryset.filter(name__icontains=value)