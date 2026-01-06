"""Support for Public Pool sensors."""
from __future__ import annotations

from datetime import datetime
import logging
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    EXA_HASH_PER_SECOND,
    GIGA_HASH_PER_SECOND,
    TERA_HASH_PER_SECOND,
)
from .coordinator import PublicPoolCoordinator

_LOGGER = logging.getLogger(__name__)

# Pool-level sensor descriptions
POOL_SENSOR_TYPES: dict[str, SensorEntityDescription] = {
    "pool_hashrate": SensorEntityDescription(
        key="pool_hashrate",
        name="Pool Hashrate",
        native_unit_of_measurement=TERA_HASH_PER_SECOND,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:speedometer",
        suggested_display_precision=2,
    ),
    "pool_miners": SensorEntityDescription(
        key="pool_miners",
        name="Pool Miners",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:account-group",
    ),
    "pool_block_height": SensorEntityDescription(
        key="pool_block_height",
        name="Pool Block Height",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:cube-outline",
    ),
}

# Network-level sensor descriptions
NETWORK_SENSOR_TYPES: dict[str, SensorEntityDescription] = {
    "network_difficulty": SensorEntityDescription(
        key="network_difficulty",
        name="Network Difficulty",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:chart-line",
        suggested_display_precision=0,
    ),
    "network_hashrate": SensorEntityDescription(
        key="network_hashrate",
        name="Network Hashrate",
        native_unit_of_measurement=EXA_HASH_PER_SECOND,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:speedometer",
        suggested_display_precision=2,
    ),
    "network_block_height": SensorEntityDescription(
        key="network_block_height",
        name="Network Block Height",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:cube",
    ),
}

# Address-level sensor descriptions
ADDRESS_SENSOR_TYPES: dict[str, SensorEntityDescription] = {
    "address_best_difficulty": SensorEntityDescription(
        key="address_best_difficulty",
        name="Best Difficulty",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:trophy",
        suggested_display_precision=2,
    ),
    "address_workers_count": SensorEntityDescription(
        key="address_workers_count",
        name="Workers Count",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:worker",
    ),
    "address_total_hashrate": SensorEntityDescription(
        key="address_total_hashrate",
        name="Total Hashrate",
        native_unit_of_measurement=GIGA_HASH_PER_SECOND,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:speedometer",
        suggested_display_precision=2,
    ),
}

# Worker sensor descriptions (template for each worker)
WORKER_SENSOR_TYPES: dict[str, SensorEntityDescription] = {
    "hashrate": SensorEntityDescription(
        key="hashrate",
        name="Hashrate",
        native_unit_of_measurement=GIGA_HASH_PER_SECOND,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:speedometer",
        suggested_display_precision=2,
    ),
    "best_difficulty": SensorEntityDescription(
        key="best_difficulty",
        name="Best Difficulty",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:trophy",
        suggested_display_precision=2,
    ),
    "last_seen": SensorEntityDescription(
        key="last_seen",
        name="Last Seen",
        device_class=SensorDeviceClass.TIMESTAMP,
        icon="mdi:clock-outline",
    ),
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Public Pool sensors from a config entry."""
    coordinator: PublicPoolCoordinator = hass.data[DOMAIN][entry.entry_id]
    
    entities = []
    
    # Add pool-level sensors
    for sensor_type, description in POOL_SENSOR_TYPES.items():
        entities.append(
            PublicPoolSensor(
                coordinator=coordinator,
                description=description,
                entry_id=entry.entry_id,
            )
        )
    
    # Add network-level sensors
    for sensor_type, description in NETWORK_SENSOR_TYPES.items():
        entities.append(
            PublicPoolSensor(
                coordinator=coordinator,
                description=description,
                entry_id=entry.entry_id,
            )
        )
    
    # Add address-level sensors
    for sensor_type, description in ADDRESS_SENSOR_TYPES.items():
        entities.append(
            PublicPoolSensor(
                coordinator=coordinator,
                description=description,
                entry_id=entry.entry_id,
            )
        )
    
    async_add_entities(entities)
    
    # Add worker sensors dynamically after first data fetch
    @callback
    def _async_add_worker_sensors():
        """Add worker sensors when workers are discovered."""
        if not coordinator.data:
            return
        
        workers = coordinator.data.get("workers", {})
        worker_entities = []
        
        for worker_name, worker_data in workers.items():
            for sensor_key, description in WORKER_SENSOR_TYPES.items():
                worker_entities.append(
                    PublicPoolWorkerSensor(
                        coordinator=coordinator,
                        description=description,
                        entry_id=entry.entry_id,
                        worker_name=worker_name,
                        sensor_key=sensor_key,
                    )
                )
        
        if worker_entities:
            async_add_entities(worker_entities)
    
    # Add worker sensors after first successful update
    coordinator.async_add_listener(_async_add_worker_sensors)


class PublicPoolSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Public Pool sensor."""

    def __init__(
        self,
        coordinator: PublicPoolCoordinator,
        description: SensorEntityDescription,
        entry_id: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry_id}_{description.key}"
        self._attr_has_entity_name = True
        
        # Device info for grouping sensors
        short_address = coordinator.bitcoin_address[:8]
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry_id)},
            "name": f"Public Pool ({short_address})",
            "manufacturer": "Public Pool",
            "model": "Bitcoin Mining Pool",
            "sw_version": "1.0",
        }

    @property
    def native_value(self) -> Any:
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return None
        return self.coordinator.data.get(self.entity_description.key)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes."""
        if not self.coordinator.data:
            return {}
        
        # Add pool blocks found as attribute for pool sensors
        if self.entity_description.key == "pool_hashrate":
            blocks = self.coordinator.data.get("pool_blocks_found", [])
            return {
                "blocks_found_count": len(blocks),
                "blocks_found": blocks,
            }
        
        return {}


class PublicPoolWorkerSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Public Pool worker sensor."""

    def __init__(
        self,
        coordinator: PublicPoolCoordinator,
        description: SensorEntityDescription,
        entry_id: str,
        worker_name: str,
        sensor_key: str,
    ) -> None:
        """Initialize the worker sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self.worker_name = worker_name
        self.sensor_key = sensor_key
        
        # Create unique ID and name
        safe_worker_name = worker_name.replace(" ", "_").lower()
        self._attr_unique_id = f"{entry_id}_worker_{safe_worker_name}_{sensor_key}"
        self._attr_name = f"{worker_name} {description.name}"
        
        # Device info for grouping worker sensors
        short_address = coordinator.bitcoin_address[:8]
        self._attr_device_info = {
            "identifiers": {(DOMAIN, f"{entry_id}_worker_{safe_worker_name}")},
            "name": f"{worker_name}",
            "manufacturer": "Public Pool",
            "model": "Mining Worker",
            "via_device": (DOMAIN, entry_id),
        }

    @property
    def native_value(self) -> Any:
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return None
        
        workers = self.coordinator.data.get("workers", {})
        worker_data = workers.get(self.worker_name)
        
        if not worker_data:
            return None
        
        value = worker_data.get(self.sensor_key)
        
        # Convert timestamp to datetime for last_seen
        if self.sensor_key == "last_seen" and value:
            try:
                return datetime.fromisoformat(value.replace("Z", "+00:00"))
            except (ValueError, AttributeError):
                return None
        
        return value

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes."""
        if not self.coordinator.data:
            return {}
        
        workers = self.coordinator.data.get("workers", {})
        worker_data = workers.get(self.worker_name)
        
        if not worker_data:
            return {}
        
        return {
            "session_id": worker_data.get("session_id"),
            "start_time": worker_data.get("start_time"),
        }

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        if not super().available:
            return False
        
        # Check if this worker still exists in the data
        if not self.coordinator.data:
            return False
        
        workers = self.coordinator.data.get("workers", {})
        return self.worker_name in workers
