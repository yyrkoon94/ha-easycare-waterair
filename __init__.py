"""
The "hello world" custom component.
This component implements the bare minimum that a component should implement.
Configuration:
To use the hello_world component you will need to add the following to your
configuration.yaml file.
easycare_waterair:
"""
from __future__ import annotations
import json
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from homeassistant.const import (
    CONF_USERNAME,
    CONF_PASSWORD,
    CONF_TOKEN
)
from homeassistant.const import Platform

from .easycare import EasyCare
from .easycare import (
    EasyCareCoordinator,
    EasyCareModuleCoordinator,
    EasyCareLightCoordinator,
)

_LOGGER = logging.getLogger("custom_components.ha-easycare-waterair")

# The domain of your component. Should be equal to the name of your component.
DOMAIN = "easycare_waterair"
COMPONENT_DATA = "easycare_waterair-data"

PLATFORMS = [
    Platform.BINARY_SENSOR,
    Platform.SENSOR,
    Platform.LIGHT,
    Platform.BUTTON,
    Platform.NUMBER
]


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up a skeleton component."""
    _LOGGER.debug("Start EasyCare component initialisation")

    # Read config
    conf = config[DOMAIN]

    # Connect to Waterair, Return boolean to indicate that initialization was successfully
    connected = await hass.async_add_executor_job(connect_easycare, hass, conf)

    if connected is False:
        return False

    # First call to API for initial datas
    easycare: EasyCare = hass.data.get(COMPONENT_DATA)
    coordinator: EasyCareCoordinator = easycare.get_coordinator()
    await coordinator.async_config_entry_first_refresh()
    module_coordinator: EasyCareModuleCoordinator = easycare.get_module_coordinator()
    await module_coordinator.async_config_entry_first_refresh()
    light_coordinator: EasyCareLightCoordinator = easycare.get_light_coordinator()
    await light_coordinator.async_config_entry_first_refresh()

    for platform in PLATFORMS:
        hass.helpers.discovery.load_platform(platform, DOMAIN, {}, config)
    _LOGGER.debug("End EasyCare component initialisation")
    return True


def connect_easycare(hass: HomeAssistant, config) -> bool:
    """Connect to easycare"""
    # Read config
    token = config.get(CONF_TOKEN)
    pool_id = config.get("pool_id")
    easycare_key = config.get("easycare_key")

    easycare = EasyCare(
        hass,
        token=token,
        easycare_key=easycare_key,
        pool_id=pool_id,
    )

    # Store EasyCare in haas data
    hass.data[COMPONENT_DATA] = easycare

    _LOGGER.debug("Calling EasyCare login")
    return easycare.connect()
