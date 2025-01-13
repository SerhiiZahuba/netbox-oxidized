from rest_framework import serializers

from netbox.api.serializers import NetBoxModelSerializer, WritableNestedSerializer

from ..models import TestNameServer, TestZone

class TestNameServerSerializer(NetBoxModelSerializer):
    class Meta:
        model = TestNameServer
        fields = (
            'id', 'name', 'url', 'display',
        )

    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_test-api:testnameserver-detail'
    )

class NestedTestNameServerSerializer(WritableNestedSerializer):
    class Meta:
        model = TestNameServer
        fields = (
            'id', 'name', 'url', 'display',
        )

    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_test-api:testnameserver-detail'
    )

class TestZoneSerializer(NetBoxModelSerializer):
    class Meta:
        model = TestZone
        fields = (
            'id', 'name', 'nameservers', 'url', 'display',
        )

    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_test-api:testzone-detail'
    )


    nameservers = NestedTestNameServerSerializer(
        many=True, read_only=True, required=False,
    )

class NestedTestZoneSerializer(WritableNestedSerializer):
    class Meta:
        model = TestZone
        fields = (
            'id', 'name', 'url', 'display',
        )

    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_test-api:testzone-detail'
    )