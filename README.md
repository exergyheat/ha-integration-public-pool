# Exergy - Public Pool

[![HACS Validation](https://github.com/exergyheat/ha-integration-public-pool/actions/workflows/validate.yml/badge.svg)](https://github.com/exergyheat/ha-integration-public-pool/actions/workflows/validate.yml)
[![GitHub Release](https://img.shields.io/github/v/release/exergyheat/ha-integration-public-pool)](https://github.com/exergyheat/ha-integration-public-pool/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Home Assistant integration for monitoring your Bitcoin miners on [Public Pool](https://web.public-pool.io).

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

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Click the three dots in the top right corner
3. Select "Custom repositories"
4. Add `https://github.com/exergyheat/ha-integration-public-pool` as an Integration
5. Click "Install"
6. Restart Home Assistant

### Manual Installation

1. Copy the `custom_components/public_pool` folder to your Home Assistant `custom_components` directory
2. Restart Home Assistant

## Configuration

1. Go to **Settings > Devices & Services**
2. Click **+ Add Integration**
3. Search for "Exergy - Public Pool"
4. Enter your Bitcoin mining address
5. (Optional) Configure pool URL (defaults to `https://web.public-pool.io`)
6. (Optional) Adjust scan interval (defaults to 60 seconds)
7. (Optional) Disable SSL verification for self-signed certificates

## Support

For issues with this Home Assistant integration: [GitHub Issues](https://github.com/exergyheat/ha-integration-public-pool/issues)

For issues with Public Pool itself: [Public Pool GitHub](https://github.com/benjamin-wilson/public-pool)

## License

MIT License - see [LICENSE](LICENSE) for details.
