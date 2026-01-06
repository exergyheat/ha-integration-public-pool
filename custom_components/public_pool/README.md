# Public Pool Home Assistant Integration

Monitor your Bitcoin miners connected to Public Pool directly in Home Assistant.

## Features

### Pool-Level Sensors
- **Pool Hashrate** - Total hashrate of the entire pool (TH/s)
- **Pool Miners** - Number of active miners on the pool
- **Pool Block Height** - Current Bitcoin block height tracked by the pool

### Network-Level Sensors
- **Network Difficulty** - Current Bitcoin network difficulty
- **Network Hashrate** - Total Bitcoin network hashrate (EH/s)
- **Network Block Height** - Current Bitcoin blockchain height

### Address-Level Sensors
- **Best Difficulty** - Highest difficulty share submitted by your miners
- **Workers Count** - Number of your active mining workers
- **Total Hashrate** - Combined hashrate of all your workers (GH/s)

### Worker Sensors (Per Miner)
For each of your mining workers, the integration creates:
- **Hashrate** - Individual worker hashrate (GH/s)
- **Best Difficulty** - Best share submitted by this worker
- **Last Seen** - Timestamp of last activity from this worker

## Installation

1. Copy the `public_pool` folder to your Home Assistant `custom_components` directory
2. Restart Home Assistant
3. Go to **Settings → Devices & Services**
4. Click **+ Add Integration**
5. Search for "Public Pool"
6. Enter your Bitcoin mining address
7. (Optional) Configure pool URL (defaults to web.public-pool.io)
8. (Optional) Adjust scan interval (defaults to 60 seconds)
9. (Optional) Disable SSL verification if using local/self-signed certificates

## Configuration

### Bitcoin Address (Required)
Your Bitcoin address that you use for mining on Public Pool.

Example: `bc1qcnpuc5scg0n4hpwpvalntmg6n0c0349x9jfgcj`

### Pool URL (Optional)
The URL of the Public Pool instance you're using.

- **Default:** `https://web.public-pool.io`
- **Custom:** Use your own Public Pool instance URL (e.g., local StartOS deployment)

### Scan Interval (Optional)
How often to poll the API for updates (in seconds).

- **Default:** 60 seconds
- **Minimum:** 30 seconds recommended

### Verify SSL (Optional)
Whether to verify SSL certificates when connecting to the pool.

- **Default:** True
- **Set to False** for local deployments with self-signed certificates

## API Endpoints Used

This integration uses the following Public Pool API endpoints:

- `/api/pool` - Pool statistics
- `/api/info` - General site information
- `/api/network` - Bitcoin network information
- `/api/client/{address}` - Your miners' information

## Example Automations

### Alert on Worker Offline
```yaml
automation:
  - alias: "Alert when miner goes offline"
    trigger:
      - platform: state
        entity_id: sensor.hk_47_last_seen
        to: "unavailable"
        for:
          minutes: 10
    action:
      - service: notify.mobile_app
        data:
          message: "Miner HK-47 appears to be offline"
```

### Track Daily Hashrate
```yaml
sensor:
  - platform: statistics
    name: "Daily Average Hashrate"
    entity_id: sensor.public_pool_total_hashrate
    state_characteristic: mean
    sampling_size: 1440  # 24 hours at 1min intervals
```

## Credits

- **Public Pool:** https://github.com/benjamin-wilson/public-pool
- **Integration Author:** @dylan

## Support

For issues with Public Pool itself, visit: https://github.com/benjamin-wilson/public-pool/issues

For issues with this Home Assistant integration, please open an issue with:
- Your Home Assistant version
- Your Public Pool version (if self-hosted)
- Relevant logs from Home Assistant
