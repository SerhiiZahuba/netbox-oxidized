# NetBox Source for Oxidized

Use NetBox as the device inventory source for [Oxidized](https://github.com/ytti/oxidized). A lightweight Python sidecar container queries the NetBox API and serves the device list over HTTP for Oxidized to consume.

## How It Works

```
┌──────────┐   HTTP GET   ┌───────────────┐  NetBox API  ┌────────┐
│ Oxidized │ ───────────► │ netbox-source │ ───────────► │ NetBox │
│          │   :8080      │  (sidecar)    │              │        │
└──────────┘              └───────────────┘              └────────┘
```

1. Oxidized is configured with an HTTP source pointing to the sidecar
2. On each refresh, Oxidized requests the device list from the sidecar
3. The sidecar queries the NetBox API with your configured filters
4. Devices are transformed to Oxidized's format: `name`, `model`, `ip`

## Quick Start

1. **Copy the example files:**

```bash
cp env.example .env
mkdir -p scripts oxidized_config
cp netbox_source.py scripts/
cp oxidized_config_example oxidized_config/config
```

2. **Edit `.env`** with your NetBox URL and API token:

```bash
NETBOX_URL=https://netbox.example.com
NETBOX_TOKEN=your_api_token_here
DOMAIN_SUFFIX=.example.com
DEVICE_FILTERS=status=active&role=router&role=switch&limit=0
```

3. **Edit `oxidized_config/config`** with your device credentials and model_map.

4. **Start the stack:**

```bash
docker-compose up -d
```

5. **Verify the device list:**

```bash
curl http://localhost:8080/
```

## Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `NETBOX_URL` | Yes | | NetBox base URL |
| `NETBOX_TOKEN` | Yes | | NetBox API token |
| `DOMAIN_SUFFIX` | No | | FQDN suffix for devices without a primary IP |
| `DEVICE_FILTERS` | No | `status=active&limit=0` | NetBox API device filters |
| `LISTEN_PORT` | No | `8080` | HTTP server port |
| `TZ` | No | `UTC` | Timezone |

### Device Filters

The `DEVICE_FILTERS` variable uses NetBox's standard [device filter parameters](https://demo.netbox.dev/static/docs/rest-api/filtering/). Some useful examples:

```bash
# All active devices
DEVICE_FILTERS=status=active&limit=0

# Only Cisco routers
DEVICE_FILTERS=status=active&role=router&manufacturer=cisco&limit=0

# Multiple roles
DEVICE_FILTERS=status=active&role=router&role=switch&role=firewall&limit=0

# Devices tagged "oxidized"
DEVICE_FILTERS=status=active&tag=oxidized&limit=0

# Devices at a specific site
DEVICE_FILTERS=status=active&site=headquarters&limit=0

# Combine multiple filters
DEVICE_FILTERS=status=active&manufacturer=cisco&region=us-west&tag=oxidized&limit=0
```

### Model Mapping

The sidecar returns the NetBox **manufacturer slug** as the `model` field. Oxidized uses `model_map` in its config to translate these to Oxidized model names:

```yaml
# oxidized_config/config
model_map:
  cisco: ios
  juniper: junos
  arista: eos
  paloaltonetworks: panos
  fortinet: fortios
```

### IP Resolution

For each device, the sidecar uses (in order):
1. **Primary IPv4 address** (CIDR notation stripped)
2. **Hostname + DOMAIN_SUFFIX** (if no primary IP and suffix is set)
3. **Hostname** (bare, as last resort)

## Standalone Usage

The script can also run outside Docker for testing:

```bash
# Set environment variables
export NETBOX_URL=https://netbox.example.com
export NETBOX_TOKEN=your_token
export DEVICE_FILTERS="status=active&role=router&limit=0"

# Print device list as JSON
python3 netbox_source.py

# Run as HTTP server
python3 netbox_source.py --serve --port 8080
```

## NetBox API Token

Create a token in NetBox under **Admin > API Tokens** (or your user profile). The token only needs **read** permissions on devices:

- `dcim.view_device` — required to list devices

## Networking

Both containers must be on the same Docker network. The `docker-compose.yaml` uses a default network. If your Oxidized and NetBox are on different networks, adjust accordingly:

```yaml
networks:
  default:
    name: your_network_name
    external: true
```
