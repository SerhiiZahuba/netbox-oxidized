from netbox.plugins import PluginConfig

class NetBoxTestConfig(PluginConfig):
    name = 'netbox_test'
    verbose_name = 'NetBox Test'
    description = 'Test plugin for demonstrating complex NetBox issues'
    author = "Peter Eckel"
    author_email = "pete@netbox-dns.org"
    version = '0.0.1'
    base_url = 'netbox_test'

config = NetBoxTestConfig