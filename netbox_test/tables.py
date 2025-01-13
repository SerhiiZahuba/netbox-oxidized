import django_tables2 as tables

from netbox.tables import NetBoxTable
from .models import TestNameServer, TestZone

class TestNameServerTable(NetBoxTable):
    name = tables.Column(
        linkify=True
    )

    class Meta(NetBoxTable.Meta):
        model = TestNameServer
        fields = ('name', )
        default_columns = ('name', )

class TestZoneTable(NetBoxTable):
    name = tables.Column(
        linkify=True
    )

    class Meta(NetBoxTable.Meta):
        model = TestZone
        fields = ('name', )
        default_columns = ('name', )