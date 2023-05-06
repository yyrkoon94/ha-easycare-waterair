"""Platform for sensor integration."""
from __future__ import annotations

import logging

from datetime import time

from homeassistant.components.time import TimeEntity

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

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
    lights = []
    modules = easycare.get_modules()
    for module in modules:
        if module.type == "lr-pc":
            # This is the BPC
            if module.number_of_inputs == 2:
                # Other exists (escalight)
                lights.append(EscalightTimerWithCoordinator(easycare))
            lights.append(SpotLightTimerWithCoordinator(easycare))

    add_entities(lights)


class SpotLightTimerWithCoordinator(CoordinatorEntity, TimeEntity):
    """Representation of a Sensor."""

    def __init__(self, easycare: EasyCare) -> None:
        """Initialize EasyCare conenction sensor."""
        super().__init__(easycare.get_coordinator())
        self._attr_name = "Easy-Care Pool Spot Timer"
        self._attr_unique_id = "easycare_pool_spot_light_timer"
        self._attr_native_value = time(0, 0)
        self._easycare = easycare
        _LOGGER.debug("EasyCare-Binary-Sensor: %s created", self.name)

    def _handle_coordinator_update(self) -> None:
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        self.async_write_ha_state()
        _LOGGER.debug("EasyCare update sensor %s", self.name)

    async def async_set_value(self, value: time) -> None:
        """Update the current value."""
        _LOGGER.debug("Update time for timer %s", self.name)


class EscalightTimerWithCoordinator(CoordinatorEntity, TimeEntity):
    """Representation of a Sensor."""

    def __init__(self, easycare: EasyCare) -> None:
        """Initialize EasyCare conenction sensor."""
        super().__init__(easycare.get_coordinator())
        self._attr_name = "Easy-Care Pool Escalight Timer"
        self._attr_unique_id = "easycare_pool_escalight_timer"
        self._attr_native_value = time(0, 0)
        self._easycare = easycare
        _LOGGER.debug("EasyCare-Binary-Sensor: %s created", self.name)

    def _handle_coordinator_update(self) -> None:
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        self.async_write_ha_state()
        _LOGGER.debug("EasyCare update sensor %s", self.name)

    async def async_set_value(self, value: time) -> None:
        """Update the current value."""
        _LOGGER.debug("Update time for timer %s", self.name)
