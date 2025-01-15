import requests

def parse_metrics(url):
    response = requests.get(url)
    data = {}
    for line in response.text.splitlines():
        if line.startswith("#") or line == "":
            continue
        parts = line.split(" ")
        if len(parts) == 2:
            key, value = parts
            data[key] = float(value) if value.replace(".", "", 1).isdigit() else value
    return data

