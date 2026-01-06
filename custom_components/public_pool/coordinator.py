"""Public Pool DataUpdateCoordinator."""
import asyncio
import logging
from datetime import timedelta
from typing import Any

import aiohttp

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import (
    API_CLIENT,
    API_INFO,
    API_NETWORK,
    API_POOL,
)

_LOGGER = logging.getLogger(__name__)

DEFAULT_DATA = {
    "bitcoin_address": None,
    # Pool data
    "pool_hashrate": 0.0,
    "pool_miners": 0,
    "pool_blocks_found": [],
    "pool_block_height": 0,
    "pool_fee": 0,
    # Network data
    "network_difficulty": 0.0,
    "network_hashrate": 0.0,
    "network_block_height": 0,
    # Address data
    "address_best_difficulty": 0.0,
    "address_workers_count": 0,
    "address_total_hashrate": 0.0,
    "workers": {},
}


class PublicPoolAPI:
    """API client for Public Pool."""

    def __init__(self, pool_url: str, bitcoin_address: str, session: aiohttp.ClientSession):
        """Initialize API."""
        self.pool_url = pool_url.rstrip("/")
        self.bitcoin_address = bitcoin_address
        self.session = session

    async def fetch_pool_info(self) -> dict[str, Any] | None:
        """Fetch pool statistics."""
        url = f"{self.pool_url}{API_POOL}"
        try:
            async with self.session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status != 200:
                    _LOGGER.error(f"HTTP {response.status} from {url}")
                    return None
                return await response.json()
        except asyncio.TimeoutError:
            _LOGGER.error(f"Timeout fetching {url}")
            return None
        except aiohttp.ClientError as err:
            _LOGGER.error(f"Client error fetching {url}: {err}")
            return None
        except Exception as err:
            _LOGGER.exception(f"Unexpected error fetching {url}: {err}")
            return None

    async def fetch_info(self) -> dict[str, Any] | None:
        """Fetch general site info."""
        url = f"{self.pool_url}{API_INFO}"
        try:
            async with self.session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status != 200:
                    _LOGGER.error(f"HTTP {response.status} from {url}")
                    return None
                return await response.json()
        except asyncio.TimeoutError:
            _LOGGER.error(f"Timeout fetching {url}")
            return None
        except aiohttp.ClientError as err:
            _LOGGER.error(f"Client error fetching {url}: {err}")
            return None
        except Exception as err:
            _LOGGER.exception(f"Unexpected error fetching {url}: {err}")
            return None

    async def fetch_network_info(self) -> dict[str, Any] | None:
        """Fetch Bitcoin network information."""
        url = f"{self.pool_url}{API_NETWORK}"
        try:
            async with self.session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status != 200:
                    _LOGGER.error(f"HTTP {response.status} from {url}")
                    return None
                return await response.json()
        except asyncio.TimeoutError:
            _LOGGER.error(f"Timeout fetching {url}")
            return None
        except aiohttp.ClientError as err:
            _LOGGER.error(f"Client error fetching {url}: {err}")
            return None
        except Exception as err:
            _LOGGER.exception(f"Unexpected error fetching {url}: {err}")
            return None

    async def fetch_client_info(self) -> dict[str, Any] | None:
        """Fetch client (address) information."""
        url = f"{self.pool_url}{API_CLIENT.format(address=self.bitcoin_address)}"
        try:
            async with self.session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status != 200:
                    _LOGGER.error(f"HTTP {response.status} from {url}")
                    return None
                return await response.json()
        except asyncio.TimeoutError:
            _LOGGER.error(f"Timeout fetching {url}")
            return None
        except aiohttp.ClientError as err:
            _LOGGER.error(f"Client error fetching {url}: {err}")
            return None
        except Exception as err:
            _LOGGER.exception(f"Unexpected error fetching {url}: {err}")
            return None


class PublicPoolCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Public Pool data."""

    def __init__(
        self,
        hass: HomeAssistant,
        bitcoin_address: str,
        pool_url: str,
        scan_interval: int,
        session: aiohttp.ClientSession,
    ) -> None:
        """Initialize coordinator."""
        self.bitcoin_address = bitcoin_address
        self.pool_url = pool_url
        self.api = PublicPoolAPI(pool_url, bitcoin_address, session)
        self._failure_count = 0
        
        super().__init__(
            hass=hass,
            logger=_LOGGER,
            name=f"Public Pool {bitcoin_address[:8]}",
            update_interval=timedelta(seconds=scan_interval),
        )

    def _parse_pool_data(self, pool_data: dict[str, Any]) -> dict[str, Any]:
        """Parse pool statistics."""
        result = {}
        
        if not pool_data:
            return result
        
        # Convert hashrate from H/s to TH/s
        result["pool_hashrate"] = float(pool_data.get("totalHashRate", 0)) / 1_000_000_000_000
        result["pool_miners"] = int(pool_data.get("totalMiners", 0))
        result["pool_blocks_found"] = pool_data.get("blocksFound", [])
        result["pool_block_height"] = int(pool_data.get("blockHeight", 0))
        result["pool_fee"] = float(pool_data.get("fee", 0))
        
        return result

    def _parse_network_data(self, network_data: dict[str, Any]) -> dict[str, Any]:
        """Parse Bitcoin network information."""
        result = {}
        
        if not network_data:
            return result
        
        result["network_difficulty"] = float(network_data.get("difficulty", 0))
        # Convert network hashrate from H/s to EH/s
        result["network_hashrate"] = float(network_data.get("networkhashps", 0)) / 1_000_000_000_000_000_000
        result["network_block_height"] = int(network_data.get("blocks", 0))
        
        return result

    def _parse_client_data(self, client_data: dict[str, Any]) -> dict[str, Any]:
        """Parse client/address information."""
        result = {}
        
        if not client_data:
            return result
        
        result["address_best_difficulty"] = float(client_data.get("bestDifficulty", 0))
        result["address_workers_count"] = int(client_data.get("workersCount", 0))
        
        # Parse workers
        workers = {}
        total_hashrate = 0.0
        
        for worker in client_data.get("workers", []):
            name = worker.get("name", "unknown")
            # Convert hashrate from H/s to GH/s
            hashrate_hs = float(worker.get("hashRate", 0))
            hashrate_ghs = hashrate_hs / 1_000_000_000
            total_hashrate += hashrate_ghs
            
            workers[name] = {
                "session_id": worker.get("sessionId"),
                "name": name,
                "best_difficulty": float(worker.get("bestDifficulty", 0)),
                "hashrate": hashrate_ghs,
                "start_time": worker.get("startTime"),
                "last_seen": worker.get("lastSeen"),
            }
        
        result["workers"] = workers
        result["address_total_hashrate"] = total_hashrate
        
        return result

    async def _async_update_data(self):
        """Fetch data from Public Pool API."""
        try:
            _LOGGER.debug(f"Fetching data for Public Pool address {self.bitcoin_address}")
            
            # Fetch all data in parallel
            pool_data, network_data, client_data = await asyncio.gather(
                self.api.fetch_pool_info(),
                self.api.fetch_network_info(),
                self.api.fetch_client_info(),
                return_exceptions=True
            )
            
            # Check for exceptions
            if isinstance(pool_data, Exception):
                _LOGGER.error(f"Error fetching pool data: {pool_data}")
                pool_data = None
            if isinstance(network_data, Exception):
                _LOGGER.error(f"Error fetching network data: {network_data}")
                network_data = None
            if isinstance(client_data, Exception):
                _LOGGER.error(f"Error fetching client data: {client_data}")
                client_data = None
            
            # If all failed, increment failure count
            if not any([pool_data, network_data, client_data]):
                self._failure_count += 1
                
                if self._failure_count == 1:
                    _LOGGER.warning(f"Public Pool API returned no data")
                    return DEFAULT_DATA.copy()
                
                raise UpdateFailed(f"Public Pool API failed")
            
            # Parse data
            data = DEFAULT_DATA.copy()
            data["bitcoin_address"] = self.bitcoin_address
            
            if pool_data:
                data.update(self._parse_pool_data(pool_data))
            
            if network_data:
                data.update(self._parse_network_data(network_data))
            
            if client_data:
                data.update(self._parse_client_data(client_data))
            
            # Reset failure count on success
            self._failure_count = 0
            
            _LOGGER.debug(
                f"Got data from Public Pool for {self.bitcoin_address}: "
                f"pool_hashrate={data.get('pool_hashrate', 0):.2f} TH/s, "
                f"address_hashrate={data.get('address_total_hashrate', 0):.2f} GH/s, "
                f"workers={len(data.get('workers', {}))}"
            )
            
            return data
            
        except Exception as err:
            self._failure_count += 1
            
            if self._failure_count == 1:
                _LOGGER.warning(f"Error fetching data from Public Pool: {err}")
                return DEFAULT_DATA.copy()
            
            _LOGGER.exception(f"Failed to fetch data from Public Pool")
            raise UpdateFailed(f"Error communicating with Public Pool API: {err}")

    @property
    def available(self) -> bool:
        """Return if Public Pool API is available."""
        return self._failure_count < 2
