from django.urls import path

from netbox.views.generic import ObjectChangeLogView

from . import views, models

urlpatterns = (
    path('test-name-servers/', views.TestNameServerListView.as_view(), name='testnameserver_list'),
    path('test-name-servers/add/', views.TestNameServerEditView.as_view(), name='testnameserver_add'),
    path('test-name-servers/<int:pk>/', views.TestNameServerView.as_view(), name='testnameserver'),
    path('test-name-servers/<int:pk>/edit/', views.TestNameServerEditView.as_view(), name='testnameserver_edit'),
    path('test-name-servers/<int:pk>/delete/', views.TestNameServerDeleteView.as_view(), name='testnameserver_delete'),
    path('test-name-servers/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='testnameserver_changelog', kwargs={
        'model': models.TestNameServer
    }),

    path("device/<int:pk>/config/", views.device_config_view, name="device_config"),
    path("status/", views.StatusView.as_view(), name="status_list"),
    path('status/add/', views.StatusCreateView.as_view(), name='status_add'),
    path('test-zones/', views.TestZoneListView.as_view(), name='testzone_list'),
    path('test-zones/add/', views.TestZoneEditView.as_view(), name='testzone_add'),
    path('test-zones/<int:pk>/', views.TestZoneView.as_view(), name='testzone'),
    path('test-zones/<int:pk>/edit/', views.TestZoneEditView.as_view(), name='testzone_edit'),
    path('test-zones/<int:pk>/delete/', views.TestZoneDeleteView.as_view(), name='testzone_delete'),
    path('test-zones/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='testzone_changelog', kwargs={
        'model': models.TestZone
    }),
)
