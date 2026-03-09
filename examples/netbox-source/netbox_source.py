#!/usr/bin/env python3
"""
NetBox to Oxidized device source.

Queries the NetBox API for devices and serves them as JSON
for Oxidized's HTTP source. Runs as a lightweight sidecar
container alongside Oxidized.

Output format (Oxidized HTTP source):
{
  "results": [
    {"name": "router01", "model": "cisco", "ip": "10.0.0.1"},
    ...
  ]
}

Fields:
  - name:  device hostname (display name in Oxidized)
  - model: manufacturer slug (maps to Oxidized model via model_map)
  - ip:    primary IPv4 address (CIDR stripped), falls back to FQDN

Usage:
  HTTP server:  python3 netbox_source.py --serve --port 8080
  One-shot:     python3 netbox_source.py

Environment variables:
  NETBOX_URL      - NetBox base URL (required)
  NETBOX_TOKEN    - NetBox API token (required)
  DOMAIN_SUFFIX   - FQDN suffix for devices without a primary IP (default: "")
  DEVICE_FILTERS  - NetBox API query string filters (default: "status=active&limit=0")
  LISTEN_PORT     - HTTP server port when using --serve (default: 8080)
"""

import argparse
import json
import os
import ssl
import sys
import urllib.error
import urllib.request

# ── Configuration (from environment) ─────────────────────────────────────────

NETBOX_URL = os.environ.get("NETBOX_URL", "").rstrip("/")
NETBOX_TOKEN = os.environ.get("NETBOX_TOKEN", "")
DOMAIN_SUFFIX = os.environ.get("DOMAIN_SUFFIX", "")
DEVICE_FILTERS = os.environ.get("DEVICE_FILTERS", "status=active&limit=0")
LISTEN_PORT = int(os.environ.get("LISTEN_PORT", "8080"))

# ── NetBox API ───────────────────────────────────────────────────────────────


def fetch_devices():
    """Fetch devices from NetBox API."""
    if not NETBOX_URL or not NETBOX_TOKEN:
        return {"error": "NETBOX_URL and NETBOX_TOKEN environment variables are required"}

    url = f"{NETBOX_URL}/api/dcim/devices/?{DEVICE_FILTERS}"
    headers = {
        "Authorization": f"Token {NETBOX_TOKEN}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    # Allow self-signed certificates
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            data = json.loads(response.read().decode())
            return data.get("results", [])
    except urllib.error.URLError as e:
        return {"error": str(e)}


# ── Transform ────────────────────────────────────────────────────────────────


def transform_devices(devices):
    """Transform NetBox devices to Oxidized HTTP source format."""
    if isinstance(devices, dict) and "error" in devices:
        return devices

    oxidized_devices = []

    for device in devices:
        name = device.get("name", "")
        if not name:
            continue

        # Primary IPv4 (strip CIDR)
        primary_ip = None
        if device.get("primary_ip4") and device["primary_ip4"].get("address"):
            primary_ip = device["primary_ip4"]["address"].split("/")[0]

        # Manufacturer slug → Oxidized model
        manufacturer = "unknown"
        if device.get("device_type") and device["device_type"].get("manufacturer"):
            manufacturer = device["device_type"]["manufacturer"].get("slug", "unknown")

        # Fall back to FQDN if no IP
        ip = primary_ip or (f"{name}{DOMAIN_SUFFIX}" if DOMAIN_SUFFIX else name)

        oxidized_devices.append(
            {
                "name": name,
                "model": manufacturer,
                "ip": ip,
            }
        )

    return {"results": oxidized_devices}


# ── HTTP server ──────────────────────────────────────────────────────────────


def serve(port):
    """Run a simple HTTP server that returns the device list on every request."""
    from http.server import BaseHTTPRequestHandler, HTTPServer

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            devices = fetch_devices()
            output = transform_devices(devices)
            payload = json.dumps(output).encode()

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

        def log_message(self, fmt, *args):
            # Minimal logging
            print(f"{self.client_address[0]} - {args[0]}")

    print(f"Serving NetBox device list on http://0.0.0.0:{port}/")
    print(f"  NETBOX_URL:      {NETBOX_URL}")
    print(f"  DEVICE_FILTERS:  {DEVICE_FILTERS}")
    print(f"  DOMAIN_SUFFIX:   {DOMAIN_SUFFIX or '(none)'}")
    HTTPServer(("0.0.0.0", port), Handler).serve_forever()


# ── CLI ──────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(description="NetBox to Oxidized HTTP source")
    parser.add_argument("--serve", action="store_true", help="Run as HTTP server")
    parser.add_argument("--port", type=int, default=LISTEN_PORT, help="Server port")
    args = parser.parse_args()

    if args.serve:
        serve(args.port)
    else:
        devices = fetch_devices()
        output = transform_devices(devices)
        print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
