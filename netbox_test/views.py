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

from django.views.generic import TemplateView
from datetime import datetime


class StatusView(TemplateView):
    template_name = "netbox_test/status_list.html"

    def get_context_data(self, **kwargs):
        from datetime import datetime
        import requests

        context = super().get_context_data(**kwargs)
        url = "http://172.26.19.4:8080/metrics"
        try:
            response = requests.get(url)
            status_data = {}
            backup_sizes = {}
            device_table = []  # Таблиця з даними пристроїв
            total_config_lines = 0
            total_backup_size = 0
            service_status = "Unknown"

            for line in response.text.splitlines():
                if line.startswith("#") or line.strip() == "":
                    continue
                parts = line.split(" ", 1)
                if len(parts) == 2:
                    key, value = parts
                    # Статус служби
                    if "oxidized_status" in key:
                        service_status = "Up" if int(value) == 1 else "Down"

                    # Дані пристроїв
                    if "oxidized_device_last_backup_status" in key:
                        full_name = key.split("{")[1].split("}")[0]
                        attributes = {kv.split("=")[0]: kv.split("=")[1].strip('"') for kv in full_name.split(",")}
                        ip = attributes.get("name", "N/A")
                        model = attributes.get("model", "N/A")
                        status = "Success" if int(value) == 2 else "Failed"

                        # Знаходимо розмір бекапу та кількість рядків
                        backup_size = 0
                        config_lines = 0
                        for line2 in response.text.splitlines():
                            if f'oxidized_device_config_size{{full_name="{attributes["full_name"]}"' in line2:
                                backup_size = int(line2.split(" ")[1])
                            if f'oxidized_device_config_lines{{full_name="{attributes["full_name"]}"' in line2:
                                config_lines = int(line2.split(" ")[1])

                        # Додаємо пристрій до таблиці
                        device_table.append({
                            "ip": ip,
                            "model": model,
                            "status": status,
                            "backup_size": backup_size / 1024,  # В кілобайтах
                            "config_lines": config_lines,
                        })

                    # Загальний розмір бекапу
                    if "oxidized_device_config_size" in key:
                        total_backup_size += int(value)

                    # Загальна кількість рядків конфігурації
                    if "oxidized_device_config_lines" in key:
                        total_config_lines += int(value)

            context["service_status"] = service_status
            context["device_table"] = device_table
            context["total_backup_size"] = total_backup_size / 1024  # В кілобайтах
            context["total_config_lines"] = total_config_lines
            context["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Час оновлення

        except Exception as e:
            context["service_status"] = "Error"
            context["device_table"] = []
            context["total_backup_size"] = 0
            context["total_config_lines"] = 0
            context["updated_at"] = "Error retrieving data"

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