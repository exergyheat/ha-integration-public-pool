"""The Public Pool integration."""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import (
    CONF_BITCOIN_ADDRESS,
    CONF_POOL_URL,
    CONF_SCAN_INTERVAL,
    CONF_VERIFY_SSL,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_VERIFY_SSL,
    DOMAIN,
    PLATFORMS,
)
from .coordinator import PublicPoolCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Public Pool from a config entry."""
    bitcoin_address = entry.data[CONF_BITCOIN_ADDRESS]
    pool_url = entry.data[CONF_POOL_URL]
    scan_interval = entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
    verify_ssl = entry.data.get(CONF_VERIFY_SSL, DEFAULT_VERIFY_SSL)
    
    _LOGGER.info(f"Setting up Public Pool for address {bitcoin_address}")
    
    # Get aiohttp session
    session = async_get_clientsession(hass, verify_ssl=verify_ssl)
    
    # Create coordinator
    coordinator = PublicPoolCoordinator(
        hass=hass,
        bitcoin_address=bitcoin_address,
        pool_url=pool_url,
        scan_interval=scan_interval,
        session=session,
    )
    
    # Store coordinator
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator
    
    # Perform initial refresh
    await coordinator.async_config_entry_first_refresh()
    
    # Forward entry setup to platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    
    return unload_ok
