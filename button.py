"""Platform for sensor integration."""

from __future__ import annotations

import logging

from homeassistant.components.button import ButtonEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from . import COMPONENT_DATA
from .easycare import EasyCare

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
    buttons = []
    buttons.append(RefreshButton(easycare, hass))

    add_entities(buttons)


class RefreshButton(ButtonEntity):
    """Representation of a Sensor."""

    def __init__(self, easycare: EasyCare, hass: HomeAssistant) -> None:
        """Initialize EasyCare refresh button."""
        self._hass = hass
        self._attr_name = "Easy-Care Pool Refresh data"
        self._attr_unique_id = "easycare_pool_refresh_button"
        self._easycare = easycare
        _LOGGER.debug("EasyCare-Button-Sensor: %s created", self.name)

    async def async_press(self) -> None:
        """Update the current value."""
        # await self._hass.async_add_executor_job(self._easycare.refresh_datas)
        await self._easycare.refresh_datas()
        _LOGGER.debug("EasyCare Refresh Button Pressed")
