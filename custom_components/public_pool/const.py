"""Constants for the Public Pool integration."""
from homeassistant.const import Platform

DOMAIN = "public_pool"

# Platforms
PLATFORMS = [Platform.SENSOR]

# Configuration
CONF_BITCOIN_ADDRESS = "bitcoin_address"
CONF_POOL_URL = "pool_url"
CONF_SCAN_INTERVAL = "scan_interval"
CONF_VERIFY_SSL = "verify_ssl"

# Defaults
DEFAULT_POOL_URL = "https://web.public-pool.io"
DEFAULT_SCAN_INTERVAL = 60  # seconds
DEFAULT_VERIFY_SSL = True

# API endpoints (relative to pool URL)
API_POOL = "/api/pool"
API_INFO = "/api/info"
API_NETWORK = "/api/network"
API_CLIENT = "/api/client/{address}"
API_SHARE_TOP = "/api/share/top-difficulties"

# Units
TERA_HASH_PER_SECOND = "TH/s"
EXA_HASH_PER_SECOND = "EH/s"
GIGA_HASH_PER_SECOND = "GH/s"

# Pool-level sensor keys
SENSOR_POOL_HASHRATE = "pool_hashrate"
SENSOR_POOL_MINERS = "pool_miners"
SENSOR_POOL_BLOCKS_FOUND = "pool_blocks_found"
SENSOR_POOL_BLOCK_HEIGHT = "pool_block_height"

# Network-level sensor keys
SENSOR_NETWORK_DIFFICULTY = "network_difficulty"
SENSOR_NETWORK_HASHRATE = "network_hashrate"
SENSOR_NETWORK_BLOCK_HEIGHT = "network_block_height"

# Address-level sensor keys
SENSOR_ADDRESS_BEST_DIFFICULTY = "best_difficulty"
SENSOR_ADDRESS_WORKERS_COUNT = "workers_count"
SENSOR_ADDRESS_TOTAL_HASHRATE = "total_hashrate"

# Worker sensor keys (per worker)
WORKER_HASHRATE = "hashrate"
WORKER_BEST_DIFFICULTY = "best_difficulty"
WORKER_LAST_SEEN = "last_seen"
