from netbox.api.viewsets import NetBoxModelViewSet

from .. import filtersets, models
from .serializers import TestNameServerSerializer, TestZoneSerializer

class TestNameServerViewSet(NetBoxModelViewSet):
    queryset = models.TestNameServer.objects.prefetch_related('tags')
    serializer_class = TestNameServerSerializer
    filterset_class = filtersets.TestNameServerFilterSet

class TestZoneViewSet(NetBoxModelViewSet):
    queryset = models.TestZone.objects.prefetch_related('tags')
    serializer_class = TestZoneSerializer
    filterset_class = filtersets.TestZoneFilterSet