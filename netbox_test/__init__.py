from netbox.plugins import PluginConfig

class NetBoxTestConfig(PluginConfig):
    name = 'netbox_test'
    verbose_name = 'NetBox Test'
    description = 'Test plugin for demonstrating complex NetBox issues'
    author = "Peter Eckel"
    author_email = "pete@netbox-dns.org"
    version = '0.0.1'
    base_url = "netbox_test"
    #    base_url = "http://oxidized.local/api/v1"  # URL вашого Oxidized
    required_settings = []
    default_settings = {
        "oxidized_url": "http://oxidized.local/api/v1",
        "oxidized_token": None,  # Якщо потрібна авторизація
    }

config = NetBoxTestConfig
