# Exergy - Public Pool

Home Assistant integration for monitoring your Bitcoin miners on a self-hosted Public Pool instance.

Tested with the Start9 Public Pool package.

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
| Pool URL | Yes | - | Your self-hosted Public Pool URL |
| Bitcoin Address | Yes | - | Your mining address |
| Scan Interval | No | 60 | Polling interval in seconds |
| Verify SSL | No | True | SSL certificate verification |

## Support

[GitHub Issues](https://github.com/exergyheat/ha-integration-public-pool/issues)
