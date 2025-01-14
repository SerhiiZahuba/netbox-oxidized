from netbox.plugins import PluginMenuButton, PluginMenuItem


testnameserver_buttons = [
    PluginMenuButton(
        link='plugins:netbox_test:testnameserver_add',
        title='Add',
        icon_class='mdi mdi-plus-thick',
    )
]

testzone_buttons = [
    PluginMenuButton(
        link='plugins:netbox_test:testzone_add',
        title='Add',
        icon_class='mdi mdi-plus-thick',
    )
]

menu_items = (
    PluginMenuItem(
        link='plugins:netbox_test:testnameserver_list',
        link_text='Test Nameservers',
        buttons=testnameserver_buttons,
    ),
    PluginMenuItem(
        link='plugins:netbox_test:testzone_list',
        link_text='Test Zones',
        buttons=testzone_buttons,
    ),
)