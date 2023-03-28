"""Platform for sensor integration."""
from __future__ import annotations

import logging

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorDeviceClass,
)

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .easycare import EasyCare

from . import (
    COMPONENT_DATA,
)

_LOGGER = logging.getLogger("custom_components.ha-easycare-waterair")


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the sensor platform."""
    easycare = hass.data.get(COMPONENT_DATA)
    sensors = []
    sensors.append(EasyCareConnectedSensor(easycare))
    async_add_entities(sensors)


class EasyCareConnectedSensor(BinarySensorEntity):
    """Representation of a Sensor."""

    def __init__(self, easycare: EasyCare) -> None:
        """Initialize EasyCare conenction sensor."""
        self._attr_name = "Easy-Care connection"
        self._attr_is_on = False
        self._attr_device_class = BinarySensorDeviceClass.CONNECTIVITY
        self._attr_icon = "mdi:network-off-outline"
        self._attr_unique_id = "EasyCare_Connection_Sensor"
        self._easycare = easycare
        _LOGGER.debug("EasyCare-Sensor: %s created", self.name)

    def update(self) -> None:
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        self._attr_icon = (
            "mdi:network-outline"
            if self._easycare.connecton_status()
            else "mdi:network-off-outline"
        )
        self._attr_is_on = self._easycare.connecton_status()
