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
)

from .easycare import EasyCare

_LOGGER = logging.getLogger("custom_components.ha-easycare-waterair")

# The domain of your component. Should be equal to the name of your component.
DOMAIN = "easycare_waterair"
COMPONENT_DATA = "easycare_waterair-data"


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up a skeleton component."""
    _LOGGER.debug("Start EasyCare component initialisation")

    # Read config
    conf = config[DOMAIN]

    # Connect to Waterair
    connected = await hass.async_add_executor_job(connect_easycare, hass, conf)

    # Return boolean to indicate that initialization was successfully.
    # user = connect_easycare(hass, config)
    if connected is False:
        return False

    _LOGGER.debug("End EasyCare component initialisation")
    return True


def connect_easycare(hass: HomeAssistant, config) -> json:
    """Connect to easycare"""
    # Read config
    username = config.get(CONF_USERNAME)
    password = config.get(CONF_PASSWORD)
    easycare_key = "NWQwMjFkYzI0NzhjMjE3MDc3MzI0NDEwOkNtVmZxNDNiZE5hUUZjWA=="

    easycare = EasyCare(username=username, password=password, easycare_key=easycare_key)

    # Store EasyCare in haas data
    hass.data[COMPONENT_DATA] = easycare

    _LOGGER.debug("Calling EasyCare login")
    return easycare.connect()
