# Public Pool Integration - Installation Guide

## ✅ Integration Created Successfully!

Your Public Pool Home Assistant integration has been created in:
```
custom_components/public_pool/
```

## 📁 Files Created

- `__init__.py` - Main integration setup
- `manifest.json` - Integration metadata
- `const.py` - Constants and configuration
- `config_flow.py` - Configuration UI flow
- `coordinator.py` - Data fetching coordinator
- `sensor.py` - Sensor entities
- `strings.json` - UI translations
- `README.md` - Documentation

## 🚀 Installation Steps

### Option 1: Already in Your Config (Current Location)
The integration is already in your custom_components directory! Just:

1. Restart Home Assistant
2. Go to **Settings → Devices & Services**
3. Click **+ Add Integration**
4. Search for "Public Pool"
5. Follow the setup wizard

### Option 2: Deploy to Your Home Assistant Server
If your Home Assistant runs elsewhere, copy the entire `public_pool` folder to:
```
/config/custom_components/public_pool/
```

Then restart Home Assistant.

## 🔧 Configuration

When adding the integration, you'll be prompted for:

### Required
- **Bitcoin Address**: Your mining address (e.g., `bc1qcnpuc5scg0n4hpwpvalntmg6n0c0349x9jfgcj`)

### Optional
- **Pool URL**: Default is `https://web.public-pool.io`
  - For your local instance: `https://bdi6s4ql7avuxquxchv26q5oqbpzlbdvmhshfezovaoz3wfrgza7z5ad.local`
- **Scan Interval**: How often to poll (default: 60 seconds)
- **Verify SSL**: Set to `false` for self-signed certificates

## 📊 Sensors Created

### Pool Level (3 sensors)
- `sensor.public_pool_pool_hashrate` - Total pool hashrate (TH/s)
- `sensor.public_pool_pool_miners` - Number of miners
- `sensor.public_pool_pool_block_height` - Current block

### Network Level (3 sensors)
- `sensor.public_pool_network_difficulty` - Bitcoin difficulty
- `sensor.public_pool_network_hashrate` - Network hashrate (EH/s)
- `sensor.public_pool_network_block_height` - Blockchain height

### Your Address (3 sensors)
- `sensor.public_pool_best_difficulty` - Your best share
- `sensor.public_pool_workers_count` - Active workers
- `sensor.public_pool_total_hashrate` - Your total hashrate (GH/s)

### Per Worker (3 sensors each)
For each worker (HK-47, IG-88, SM-33, T3-M4, Bedroom_Nano3s):
- `sensor.{worker_name}_hashrate` - Worker hashrate (GH/s)
- `sensor.{worker_name}_best_difficulty` - Best share
- `sensor.{worker_name}_last_seen` - Last activity timestamp

**Total:** ~18 sensors (3+3+3 base + 3×5 workers = 18 sensors)

## 🧪 Testing

After setup, check the integration:

1. Go to **Developer Tools → States**
2. Search for `public_pool`
3. Verify sensors are populated with data

## 🐛 Troubleshooting

### SSL Certificate Errors
If using your local .onion address:
- Set **Verify SSL** to `false` during setup

### No Data Showing
1. Check Home Assistant logs: **Settings → System → Logs**
2. Search for "public_pool" errors
3. Verify your Bitcoin address is actively mining

### Workers Not Appearing
- Workers are created dynamically after the first data fetch
- Wait 60 seconds after setup for initial refresh
- Restart Home Assistant if workers don't appear

## 📈 Example Dashboard Card

```yaml
type: entities
title: Public Pool Mining
entities:
  - sensor.public_pool_total_hashrate
  - sensor.public_pool_workers_count
  - sensor.public_pool_best_difficulty
  - sensor.hk_47_hashrate
  - sensor.ig_88_hashrate
  - sensor.sm_33_hashrate
  - sensor.t3_m4_hashrate
  - sensor.bedroom_nano3s_hashrate
```

## 🎯 Next Steps

1. Install the integration in Home Assistant
2. Add it to your dashboard
3. Set up automations for offline alerts
4. Monitor your mining performance!

## 📝 Notes

- The integration uses the Public Pool REST API
- All data is read-only (no configuration changes to your miners)
- Worker sensors update every 60 seconds by default
- SSL verification can be disabled for local/self-signed certificates

Enjoy monitoring your Bitcoin mining operation! ⚡🚀
