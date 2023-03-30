import logging
from homeassistant.core import HomeAssistant
from .config import EasyCareConfig
from .connect import Connect
from .coordinator import EasyCareCoordinator
from .model.client import Client
from .model.pool import Pool
from datetime import timedelta

_LOGGER = logging.getLogger("custom_components.ha-easycare-waterair")

SCAN_INTERVAL = timedelta(seconds=60)


class EasyCare:
    """Entry point for all Easy-Care operations."""

    def __init__(self, hass: HomeAssistant, **kwargs) -> None:
        """Constructor for the Easy-Care object."""
        _LOGGER.debug("EasyCare component initialisation")

        # Set up the config first.
        self._cfg = EasyCareConfig(**kwargs)
        self._connect = Connect(self._cfg)
        self._coordinator = EasyCareCoordinator(hass, self._cfg, self._connect)
        self._client = None
        self._pool = None

    def connect(self) -> bool:
        """Call the connect api for the first login"""
        return self._connect.login()

    def get_connection_status(self) -> bool:
        """Return the connextion status for Easy-Care"""
        return self._connect.get_connection_status()

    def get_coordinator(self) -> bool:
        """Return the connextion status for Easy-Care"""
        return self._coordinator

    def initialize(self) -> None:
        """Initialization with static values"""
        self.get_client()

    def get_client(self) -> Client:
        """Return the Pool Owner"""
        if self._client is not None:
            return self._client

        client_response = self._connect.easycare_get_user()
        if client_response is None:
            self._client = Client(None)
            self._pool = Pool(None)
        else:
            self._client = Client(client_response)
            # Check if the pool exists
            if len(client_response["pools"]) < self._cfg.pool_id:
                self._pool = Pool(None)
            else:
                self._pool = Pool(client_response["pools"][self._cfg.pool_id - 1])
        return self._client

    def get_pool(self) -> Pool:
        """Return the Pool Detail"""
        return self._pool
