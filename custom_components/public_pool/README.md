# Exergy - Public Pool

Home Assistant integration for monitoring your Bitcoin miners on Public Pool.

## Sensors

### Pool Level
- Pool Hashrate (TH/s)
- Pool Miners
- Pool Block Height

### Network Level
- Network Difficulty
- Network Hashrate (EH/s)
- Network Block Height

### Address Level
- Best Difficulty
- Workers Count
- Total Hashrate (GH/s)

### Per Worker
- Hashrate (GH/s)
- Best Difficulty
- Last Seen

## Configuration Options

| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| Bitcoin Address | Yes | - | Your mining address |
| Pool URL | No | `https://web.public-pool.io` | Pool API URL |
| Scan Interval | No | 60 | Polling interval in seconds |
| Verify SSL | No | True | SSL certificate verification |

## Support

[GitHub Issues](https://github.com/exergyheat/ha-integration-public-pool/issues)
