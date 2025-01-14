# netbox-oxidized


1) cd /opt
2) git clone
3) cd /opt/netbox-oxidized
4) source /opt/netbox/venv/bin/activate
5) pip install .
6) add to
   vim /opt/netbox/netbox/netbox/configuration.py
   netbox_test
7) python3 /opt/netbox/netbox/manage.py migrate
8) restart netbox ()