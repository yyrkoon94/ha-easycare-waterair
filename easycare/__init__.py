import logging
from homeassistant.core import HomeAssistant
from .config import EasyCareConfig
from .connect import Connect
from .coordinator import EasyCareCoordinator
from .model.client import Client
from .model.pool import Pool
from .model.metrics import Metrics
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
        self._client = None
        self._pool = None
        self._metrics = None
        self._coordinator = EasyCareCoordinator(hass, self._cfg, self._connect)

    def initialize(self) -> None:
        """Initialization with firsts values"""
        self._connect.easycare_update_user()

    def get_coordinator(self) -> bool:
        """Return the connextion status for Easy-Care"""
        return self._coordinator

    def connect(self) -> bool:
        """Call the connect api for the first login"""
        return self._connect.login()

    def get_connection_status(self) -> bool:
        """Return the connextion status for Easy-Care"""
        return self._connect.get_connection_status()

    def get_client(self) -> Client:
        """Return the Pool Owner"""
        if self._client is not None:
            return self._client
        user_json = self._connect.get_user_json()
        if user_json is None:
            self._client = Client(None)
        else:
            self._client = Client(user_json)
        return self._client

    def get_pool(self) -> Pool:
        """Return the Pool Detail"""
        if self._pool is not None:
            return self._pool
        user_json = self._connect.get_user_json()
        if user_json is None:
            self._pool = Pool(None)
        else:
            # Check if the pool exists
            if len(user_json["pools"]) < self._cfg.pool_id:
                self._pool = Pool(None)
            else:
                self._pool = Pool(user_json["pools"][self._cfg.pool_id - 1])
        return self._pool

    def get_pool_metrics(self) -> Metrics:
        """Return metrics Detail"""
        user_json = self._connect.get_user_json()
        if user_json is None:
            if self._metrics is None:
                self._metrics = Metrics(None)
        else:
            if len(user_json["pools"]) < self._cfg.pool_id:
                if self._metrics is None:
                    self._metrics = Metrics(None)
            else:
                self._metrics = Metrics(user_json["pools"][self._cfg.pool_id - 1])
        return self._metrics
