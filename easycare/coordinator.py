"""Example integration using DataUpdateCoordinator."""

from datetime import timedelta
import logging

from async_timeout import timeout
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from homeassistant.core import HomeAssistant
from .config import EasyCareConfig
from .connect import Connect

_LOGGER = logging.getLogger("custom_components.ha-easycare-waterair")


class EasyCareCoordinator(DataUpdateCoordinator):
    """My custom coordinator."""

    def __init__(
        self,
        hass: HomeAssistant,
        config: EasyCareConfig,
        connect: Connect,
    ) -> None:
        """Initialize my coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            # Name of the data. For logging purposes.
            name="EasyCare_Cooridnator",
            # Polling interval. Will only be polled if there are subscribers.
            update_interval=timedelta(seconds=1800),  # every 30 minutes
        )
        self._hass = hass
        self._cfg = config
        self._connect = connect

    async def _async_update_data(self):
        """Fetch data from API endpoint.

        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.
        """
        _LOGGER.debug("Calling DataCoordinator to update data API")
        async with timeout(10):
            await self._hass.async_add_executor_job(self._connect.easycare_update_user)


class EasyCareModuleCoordinator(DataUpdateCoordinator):
    """My custom coordinator."""

    def __init__(
        self,
        hass: HomeAssistant,
        config: EasyCareConfig,
        connect: Connect,
    ) -> None:
        """Initialize my coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            # Name of the data. For logging purposes.
            name="EasyCare_Cooridnator",
            # Polling interval. Will only be polled if there are subscribers.
            update_interval=timedelta(seconds=86400),  # Once a day
        )
        self._hass = hass
        self._cfg = config
        self._connect = connect

    async def _async_update_data(self):
        """Fetch data from API endpoint.

        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.
        """
        _LOGGER.debug("Calling DataCoordinator to update data API")
        async with timeout(10):
            await self._hass.async_add_executor_job(
                self._connect.easycare_update_modules
            )
