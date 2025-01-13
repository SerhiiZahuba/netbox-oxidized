from netbox.api.routers import NetBoxRouter

from . import views

app_name = 'netbox_test'

router = NetBoxRouter()
router.register('test-name-servers', views.TestNameServerViewSet)
router.register('test-zones', views.TestZoneViewSet)

urlpatterns = router.urls