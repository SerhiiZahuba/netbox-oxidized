from django import forms

from utilities.forms.fields import DynamicModelMultipleChoiceField
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm

from .models import TestNameServer, TestZone

class TestNameServerForm(NetBoxModelForm):
    class Meta:
        model = TestNameServer
        fields = ('name', )

class TestZoneForm(NetBoxModelForm):
    class Meta:
        model = TestZone
        fields = ('name', 'nameservers')

    nameservers = DynamicModelMultipleChoiceField(
        queryset=TestNameServer.objects.all(),
        required=False,
    )

class TestNameServerFilterForm(NetBoxModelFilterSetForm):
    model=TestNameServer

    name = forms.CharField(
        required=False
    )

class TestZoneFilterForm(NetBoxModelFilterSetForm):
    model=TestZone

    name = forms.CharField(
        required=False
    )