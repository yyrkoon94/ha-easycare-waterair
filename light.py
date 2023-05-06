"""Platform for sensor integration."""
from __future__ import annotations

import logging

from homeassistant.components.light import (
    LightEntity,
    ColorMode,
)

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
                lights.append(EscalightSensorWithCoordinator(easycare))
            lights.append(SpotLightSensorWithCoordinator(easycare))

    add_entities(lights)


class SpotLightSensorWithCoordinator(CoordinatorEntity, LightEntity):
    """Representation of a Sensor."""

    def __init__(self, easycare: EasyCare) -> None:
        """Initialize EasyCare conenction sensor."""
        super().__init__(easycare.get_coordinator())
        self._attr_name = "Easy-Care Pool Spot"
        self._attr_unique_id = "easycare_pool_spot_light"
        self._attr_icon = "mdi:lightbulb-on"
        self._attr_is_on = False
        self._attr_color_mode = ColorMode.ONOFF
        self._easycare = easycare
        _LOGGER.debug("EasyCare-Binary-Sensor: %s created", self.name)

    def _handle_coordinator_update(self) -> None:
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        self.async_write_ha_state()
        _LOGGER.debug("EasyCare update sensor %s", self.name)

    async def async_turn_on(self, **kwargs):
        """Turn device on."""
        # duration = kwargs.get("duration", 3600)
        self._attr_is_on = True
        self.async_write_ha_state()
        _LOGGER.debug("EasyCare turn on light %s", self.name)

    async def async_turn_off(self, **kwargs):
        """Turn device on."""
        self._attr_is_on = False
        self.async_write_ha_state()
        _LOGGER.debug("EasyCare turn off light %s", self.name)


class EscalightSensorWithCoordinator(CoordinatorEntity, LightEntity):
    """Representation of a Sensor."""

    def __init__(self, easycare: EasyCare) -> None:
        """Initialize EasyCare conenction sensor."""
        super().__init__(easycare.get_coordinator())
        self._attr_name = "Easy-Care Pool Escalight"
        self._attr_unique_id = "easycare_pool_escalight"
        self._attr_icon = "mdi:light-recessed"
        self._attr_is_on = False
        self._attr_color_mode = ColorMode.ONOFF
        self._easycare = easycare
        _LOGGER.debug("EasyCare-Binary-Sensor: %s created", self.name)

    def _handle_coordinator_update(self) -> None:
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        self.async_write_ha_state()
        _LOGGER.debug("EasyCare update sensor %s", self.name)

    async def async_turn_on(self, **kwargs):
        """Turn device on."""
        # duration = kwargs.get("duration", 3600)
        self._attr_is_on = True
        self.async_write_ha_state()
        _LOGGER.debug("EasyCare turn on light %s", self.name)

    async def async_turn_off(self, **kwargs):
        """Turn device on."""
        self._attr_is_on = False
        self.async_write_ha_state()
        _LOGGER.debug("EasyCare turn off light %s", self.name)
