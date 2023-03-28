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
import time
import logging
import requests

from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from homeassistant.const import (
    CONF_USERNAME,
    CONF_PASSWORD,
)

_LOGGER = logging.getLogger(__name__)

# The domain of your component. Should be equal to the name of your component.
DOMAIN = "easycare_waterair"
DEFAULT_HOST = "https://easycare.waterair.com"


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up a skeleton component."""
    # States are in the format DOMAIN.OBJECT_ID.
    hass.states.async_set("easycare_waterair.Connected", "Works!")

    # Connect to Waterair
    user = await hass.async_add_executor_job(connect_easycare, hass, config)
    # if easycare is None:
    #    return False

    # Return boolean to indicate that initialization was successfully.
    # user = connect_easycare(hass, config)
    if user is False:
        hass.states.async_set("easycare_waterair.Connected", "Unable to connect :(")
        return False
    else:
        _LOGGER.debug("Bearer : %s", user["access_token"])
        return True


def connect_easycare(hass, config) -> json:
    """Connect to easycare"""
    # Read config
    username = config.get(CONF_USERNAME)
    password = config.get(CONF_PASSWORD)
    # host = conf.get(CONF_HOST)

    easycare_key = "NWQwMjFkYzI0NzhjMjE3MDc3MzI0NDEwOkNtVmZxNDNiZE5hUUZjWA=="
    _LOGGER.debug("Call easycare_login")
    return easycare_login(username, password, easycare_key)


def easycare_login(username, password, easycare_key) -> json:
    """Connect to easycare"""
    return False
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "connected-pool-waterair/2.4.6 (iPad; iOS 16.3; Scale/2.00)",
        "authorization": "Basic " + easycare_key,
    }

    attempt = 0
    login = None
    while attempt < 1:
        attempt += 1
        _LOGGER.debug("login attempt #%s", attempt)
        login = requests.post(
            DEFAULT_HOST + "/oauth2/token",
            json={
                "scope": "email",
                "password": password,
                "username": username,
                "grant_type": "password",
            },
            headers=headers,
            timeout=3,
            verify=False,
        )
        if login is not None:
            break
        time.sleep(1)
    if login is None:
        _LOGGER.debug("Authentication failed")
        return False
    if login.status_code != 200:
        _LOGGER.debug("Request failed, status_code is %s", login.status_code)
        return False

    _LOGGER.debug("Authentication done !")
    return json.loads(login.content)
