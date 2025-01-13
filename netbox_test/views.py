from netbox.views import generic
from . import forms, models, tables, filtersets

class TestNameServerView(generic.ObjectView):
    queryset = models.TestNameServer.objects.all()

class TestNameServerListView(generic.ObjectListView):
    queryset = models.TestNameServer.objects.all()
    table = tables.TestNameServerTable
    filterset = filtersets.TestNameServerFilterSet
    filterset_form = forms.TestNameServerFilterForm

class TestNameServerEditView(generic.ObjectEditView):
    queryset = models.TestNameServer.objects.all()
    form = forms.TestNameServerForm

class TestNameServerDeleteView(generic.ObjectDeleteView):
    queryset = models.TestNameServer.objects.all()

class TestZoneView(generic.ObjectView):
    queryset = models.TestZone.objects.all()

class TestZoneListView(generic.ObjectListView):
    queryset = models.TestZone.objects.all()
    table = tables.TestZoneTable
    filterset = filtersets.TestZoneFilterSet
    filterset_form = forms.TestZoneFilterForm

class TestZoneEditView(generic.ObjectEditView):
    queryset = models.TestZone.objects.all()
    form = forms.TestZoneForm

class TestZoneDeleteView(generic.ObjectDeleteView):
    queryset = models.TestZone.objects.all()