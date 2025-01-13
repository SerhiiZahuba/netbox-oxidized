from django.db import models
from django.urls import reverse

from netbox.models import NetBoxModel

class TestNameServer(NetBoxModel):
    def get_absolute_url(self):
        return reverse('plugins:netbox_test:testnameserver', args=[self.pk])

    def __str__(self):
        return self.name

    name = models.CharField(
        max_length=256,
    )

class TestZone(NetBoxModel):
    def get_absolute_url(self):
        return reverse('plugins:netbox_test:testzone', args=[self.pk])

    def __str__(self):
        return self.name

    name = models.CharField(
        max_length=256,
    )
    nameservers = models.ManyToManyField(
        to=TestNameServer,
        blank=True,
    )