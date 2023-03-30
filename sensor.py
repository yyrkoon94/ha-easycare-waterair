"""Platform for SensorEnity integration."""
from __future__ import annotations

import logging

from homeassistant.components.sensor import SensorEntity

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .easycare import EasyCare

from . import (
    COMPONENT_DATA,
)

_LOGGER = logging.getLogger("custom_components.ha-easycare-waterair")


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the sensor platform."""
    # We only want this platform to be set up via discovery.
    easycare: EasyCare = hass.data.get(COMPONENT_DATA)
    sensors = []
    # MyEntity(coordinator, idx) for idx, ent in enumerate(easycare.get_coordinator().data)
    sensors.append(StaticPoolOwner(easycare))
    sensors.append(StaticPoolDetail(easycare))
    add_entities(sensors)


class StaticPoolOwner(SensorEntity):
    """Representation of a Sensor."""

    def __init__(self, easycare: EasyCare) -> None:
        """Pool Owner sensor."""
        client = easycare.get_client()
        self._attr_name = "Pool Owner"
        self._attr_icon = "mdi:account"
        self._attr_unique_id = "pool_owner_sensor"
        if client.is_filled:
            self._attr_native_value = client.first_name + " " + client.last_name
            self._attr_extra_state_attributes = {
                "client_address": client.address_line1
                + " "
                + client.address_line2
                + ", "
                + client.postal_code
                + " "
                + client.city,
                "client_email": client.email,
            }
        else:
            self._attr_available = False
        self._easycare = easycare
        _LOGGER.debug("Easy-Care Sensor %s created", self.name)


class StaticPoolDetail(SensorEntity):
    """Representation of a Sensor."""

    def __init__(self, easycare: EasyCare) -> None:
        """Pool Owner sensor."""
        pool = easycare.get_pool()
        self._attr_name = "Pool Detail"
        self._attr_icon = "mdi:pool"
        self._attr_unique_id = "pool_detail_sensor"
        if easycare.get_pool().is_filled:
            self._attr_native_value = pool.model
            self._attr_extra_state_attributes = {
                "pool_address": pool.address,
                "pool_longitude": pool.longitude,
                "pool_latitude": pool.latitude,
                "pool_custom_photo": pool.custom_photo,
                "pool_volume": pool.volume,
            }
        else:
            self._attr_available = False
        self._easycare = easycare
        _LOGGER.debug("Easy-Care Sensor %s created", self.name)
