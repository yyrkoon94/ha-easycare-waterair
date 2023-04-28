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
            update_interval=timedelta(seconds=1800),
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
        # self._connect._is_connected = (
        #    False if self._connect._is_connected is True else True
        # )
        # await self._connect.easycare_update_user()
        # try:
        # Note: asyncio.TimeoutError and aiohttp.ClientError are already
        # handled by the data update coordinator.
        async with timeout(10):
            # Grab active context variables to limit data required to be fetched from API
            # Note: using context is not required if there is no need or ability to limit
            # data retrieved from API.

            await self._hass.async_add_executor_job(self._connect.easycare_update_user)
            return "ok"
        # except ApiAuthError as err:
        # Raising ConfigEntryAuthFailed will cancel future updates
        # and start a config flow with SOURCE_REAUTH (async_step_reauth)

    #     raise ConfigEntryAuthFailed from err
    # except ApiError as err:
    #    raise UpdateFailed(f"Error communicating with API: {err}")
