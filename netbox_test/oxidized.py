import requests
from django.conf import settings

def get_device_config(device_name):
    base_url = settings.PLUGINS_CONFIG["netbox_test"]["oxidized_url"]
    headers = {
        "Content-Type": "application/json",
    }
    # Якщо використовується токен
    if settings.PLUGINS_CONFIG["netbox_test"].get("oxidized_token"):
        headers["Authorization"] = f"Bearer {settings.PLUGINS_CONFIG['netbox_test']['oxidized_token']}"

    response = requests.get(f"{base_url}/node/show/{device_name}?format=json", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.text}
