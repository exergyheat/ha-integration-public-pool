"""Config flow for Public Pool integration."""
from __future__ import annotations

import logging
from typing import Any

import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import (
    CONF_BITCOIN_ADDRESS,
    CONF_POOL_URL,
    CONF_SCAN_INTERVAL,
    CONF_VERIFY_SSL,
    DEFAULT_POOL_URL,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_VERIFY_SSL,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_BITCOIN_ADDRESS): str,
        vol.Optional(CONF_POOL_URL, default=DEFAULT_POOL_URL): str,
        vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): int,
        vol.Optional(CONF_VERIFY_SSL, default=DEFAULT_VERIFY_SSL): bool,
    }
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """
    bitcoin_address = data[CONF_BITCOIN_ADDRESS]
    pool_url = data[CONF_POOL_URL].rstrip("/")
    verify_ssl = data.get(CONF_VERIFY_SSL, DEFAULT_VERIFY_SSL)
    
    # Test API connection
    session = async_get_clientsession(hass, verify_ssl=verify_ssl)
    url = f"{pool_url}/api/client/{bitcoin_address}"
    
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
            if response.status == 404:
                raise ValueError("Bitcoin address not found or invalid")
            if response.status != 200:
                raise ValueError(f"API returned HTTP {response.status}")
            
            api_data = await response.json()
            
            # Check if we got valid data
            if "workersCount" not in api_data and "workers" not in api_data:
                raise ValueError("Invalid API response")
            
    except aiohttp.ClientError as err:
        _LOGGER.error(f"Error connecting to Public Pool API: {err}")
        raise ValueError("Cannot connect to Public Pool API")
    except Exception as err:
        _LOGGER.error(f"Unexpected error: {err}")
        raise ValueError(f"Unexpected error: {err}")
    
    # Return info that you want to store in the config entry.
    # Shorten address for display
    short_address = f"{bitcoin_address[:8]}...{bitcoin_address[-8:]}"
    return {"title": f"Public Pool ({short_address})"}


class PublicPoolConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Public Pool."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except ValueError as err:
                _LOGGER.error(f"Validation failed: {err}")
                errors["base"] = "cannot_connect"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception during validation")
                errors["base"] = "unknown"
            else:
                # Set unique ID to prevent duplicate entries
                await self.async_set_unique_id(user_input[CONF_BITCOIN_ADDRESS])
                self._abort_if_unique_id_configured()
                
                return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )
