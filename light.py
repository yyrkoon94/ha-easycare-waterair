"""Platform for sensor integration."""

from __future__ import annotations

import logging

from homeassistant.components.light import ColorMode, LightEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

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
    lights = []
    modules = easycare.get_modules()
    if modules:
        for module in modules:
            if module.type == "lr-pc":
                # This is the BPC
                if module.number_of_inputs == 2:
                    # Other exists (escalight)
                    lights.append(EscalightSensorWithCoordinator(easycare, hass))
                lights.append(SpotLightSensorWithCoordinator(easycare, hass))

    add_entities(lights)


class SpotLightSensorWithCoordinator(CoordinatorEntity, LightEntity):
    """Representation of a Sensor."""

    def __init__(self, easycare: EasyCare, hass: HomeAssistant) -> None:
        """Initialize EasyCare conenction sensor."""
        super().__init__(easycare.get_light_coordinator())
        self._hass = hass
        self._easycare = easycare
        self._attr_name = "Easy-Care Pool Spot"
        self._attr_unique_id = "easycare_pool_spot_light"
        self._attr_icon = "mdi:lightbulb-on"
        bpc_modules = self._easycare.get_bpc_modules()
        module = bpc_modules[1]
        if module["time"] != "00:00":
            self._attr_is_on = True
        else:
            self._attr_is_on = False
        self._attr_color_mode = ColorMode.ONOFF
        self._attr_supported_color_modes = ColorMode.ONOFF
        self._attr_extra_state_attributes = {"remaining_time": module["time"]}
        _LOGGER.debug("EasyCare-Binary-Sensor: %s created", self.name)

    def _handle_coordinator_update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        bpc_modules = self._easycare.get_bpc_modules()
        module = bpc_modules[1]
        if module["time"] != "00:00" and self._attr_is_on is False:
            self._attr_is_on = True
        if module["time"] == "00:00" and self._attr_is_on is True:
            self._attr_is_on = False

        if self._attr_extra_state_attributes["remaining_time"] != module["time"]:
            self._attr_extra_state_attributes = {"remaining_time": module["time"]}
        self.async_write_ha_state()
        _LOGGER.debug("EasyCare update sensor %s", self.name)

    async def async_turn_on(self, **kwargs):
        """Turn device on."""
        # duration = kwargs.get("duration", 3600)
        status = await self._hass.async_add_executor_job(
            self._easycare.turn_on_module, self._easycare.get_modules(), 1
        )
        duration = 1
        number = self._hass.states.get(
            "number.easy_care_pool_spot_light_duration_in_hours"
        )
        if number is not None:
            duration = str(int(float(number.state)))
        self._attr_is_on = status
        self._attr_extra_state_attributes = {"remaining_time": "0" + duration + ":00"}
        self.async_write_ha_state()
        _LOGGER.debug("EasyCare turn on light %s", self.name)

    async def async_turn_off(self, **kwargs):
        """Turn device on."""
        status = await self._hass.async_add_executor_job(
            self._easycare.turn_off_module, self._easycare.get_modules(), 1
        )
        if status is True:
            self._attr_is_on = False
            self._attr_extra_state_attributes = {"remaining_time": "00:00"}
            self.async_write_ha_state()
            _LOGGER.debug("EasyCare turn off light %s", self.name)


class EscalightSensorWithCoordinator(CoordinatorEntity, LightEntity):
    """Representation of a Sensor."""

    def __init__(self, easycare: EasyCare, hass: HomeAssistant) -> None:
        """Initialize EasyCare conenction sensor."""
        super().__init__(easycare.get_light_coordinator())
        self._hass = hass
        self._easycare = easycare
        self._attr_name = "Easy-Care Pool Escalight"
        self._attr_unique_id = "easycare_pool_escalight"
        self._attr_icon = "mdi:light-recessed"
        bpc_modules = self._easycare.get_bpc_modules()
        module = bpc_modules[2]
        if module["time"] != "00:00":
            self._attr_is_on = True
        else:
            self._attr_is_on = False
        self._attr_color_mode = ColorMode.ONOFF
        self._attr_supported_color_modes = ColorMode.ONOFF
        self._attr_extra_state_attributes = {"remaining_time": module["time"]}
        _LOGGER.debug("EasyCare-Binary-Sensor: %s created", self.name)

    def _handle_coordinator_update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        bpc_modules = self._easycare.get_bpc_modules()
        module = bpc_modules[2]
        if module["time"] != "00:00" and self._attr_is_on is False:
            self._attr_is_on = True
        if module["time"] == "00:00" and self._attr_is_on is True:
            self._attr_is_on = False

        if self._attr_extra_state_attributes["remaining_time"] != module["time"]:
            self._attr_extra_state_attributes = {"remaining_time": module["time"]}
        self.async_write_ha_state()
        _LOGGER.debug("EasyCare update sensor %s", self.name)

    async def async_turn_on(self, **kwargs):
        """Turn device on."""
        # duration = kwargs.get("duration", 3600)
        status = await self._hass.async_add_executor_job(
            self._easycare.turn_on_module, self._easycare.get_modules(), 2
        )
        duration = 1
        number = self._hass.states.get(
            "number.easy_care_pool_escalight_light_duration_in_hours"
        )
        if number is not None:
            duration = str(int(float(number.state)))
        self._attr_is_on = status
        self._attr_extra_state_attributes = {"remaining_time": "0" + duration + ":00"}
        self.async_write_ha_state()
        _LOGGER.debug("EasyCare turn on light %s", self.name)

    async def async_turn_off(self, **kwargs):
        """Turn device on."""
        status = await self._hass.async_add_executor_job(
            self._easycare.turn_off_module, self._easycare.get_modules(), 2
        )
        if status is True:
            self._attr_is_on = False
            self._attr_extra_state_attributes = {"remaining_time": "00:00"}
            self.async_write_ha_state()
            _LOGGER.debug("EasyCare turn off light %s", self.name)
