from netbox.views import generic
from . import forms, models, tables, filtersets
from .oxidized import get_device_config


from django.views.generic import ListView, CreateView
from .models import Status


import requests
import json
from django.shortcuts import render
from django.http import HttpResponse

from .utils import parse_metrics

from django.shortcuts import render

class StatusView(TemplateView):
    template_name = "netbox_test/status_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url = "http://172.26.19.4:8080/metrics"
        try:
            response = requests.get(url)
            status_data = {}
            backup_sizes = {}
            oxidized_status = 0  # За замовчуванням

            for line in response.text.splitlines():
                if line.startswith("#") or line.strip() == "":
                    continue
                parts = line.split(" ", 1)
                if len(parts) == 2:
                    key, value = parts
                    if "status" in key and key != "oxidized_status":
                        status_data[key] = float(value) if value.replace('.', '', 1).isdigit() else 0
                    elif "backup_size" in key:
                        backup_sizes[key] = float(value) if value.replace('.', '', 1).isdigit() else 0
                    elif key == "oxidized_status":
                        oxidized_status = int(value) if value.isdigit() else 0

            # Додаємо обробку статусу служби
            context["status"] = status_data
            context["backup_sizes"] = backup_sizes
            context["service_status"] = "Up" if oxidized_status == 1 else "Down"

        except Exception as e:
            context["status"] = {}
            context["backup_sizes"] = {}
            context["service_status"] = "Down"  # Якщо є помилка, вважаємо, що служба не працює

        return context




class StatusListView(ListView):
    model = Status
    template_name = 'netbox_test/status_list.html'

class StatusCreateView(CreateView):
    model = Status
    fields = ['name', 'description']
    template_name = 'netbox_test/status_form.html'


def device_config_view(request, pk):
    device_name = "example-device"  # Отримайте ім'я пристрою з бази
    config = get_device_config(device_name)

    return render(request, "netbox_test/device_config.html", {"config": config})

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