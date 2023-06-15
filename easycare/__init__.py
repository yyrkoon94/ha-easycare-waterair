import logging
from homeassistant.core import HomeAssistant
from .config import EasyCareConfig
from .connect import Connect
from .coordinator import (
    EasyCareCoordinator,
    EasyCareModuleCoordinator,
    EasyCareLightCoordinator,
)
import json
from .model.client import Client
from .model.pool import Pool
from .model.metrics import Metrics
from .model.alerts import Alerts
from .model.treatment import Treatment
from .model.module import Module
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
        self._hass = hass
        self._connect = Connect(self._cfg, self._hass)
        self._client = None
        self._pool = None
        self._metrics = None
        self._alerts = None
        self._treatment = None
        self._modules = []
        self._coordinator = EasyCareCoordinator(hass, self._cfg, self._connect)
        self._module_coordinator = EasyCareModuleCoordinator(
            hass, self._cfg, self._connect
        )
        self._light_coordinator = EasyCareLightCoordinator(
            hass, self._cfg, self._connect
        )

    def initialize(self) -> None:
        """Initialization with firsts values"""
        self._connect.easycare_update_user()

    def get_coordinator(self) -> bool:
        """Return the coordianteur for live datas"""
        return self._coordinator

    def get_module_coordinator(self) -> bool:
        """Return the coordinator for module datas"""
        return self._module_coordinator

    def get_light_coordinator(self) -> bool:
        """Return the coordinator for lights datas"""
        return self._light_coordinator

    def connect(self) -> bool:
        """Call the connect api for the first login"""
        return self._connect.login()

    def get_modules(self):
        """Return modules array"""
        modules = self._connect.get_modules()
        self._modules = []
        for module in modules:
            self._modules.append(Module(module))
        return self._modules

    def get_connection_status(self) -> bool:
        """Return the connection status for Easy-Care"""
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

    def get_bpc_modules(self) -> json:
        """Return the bpc modules in json"""
        return self._connect.get_bpc_modules()

    def get_alerts(self) -> Alerts:
        """Return alerts Detail"""
        user_json = self._connect.get_user_json()
        if user_json is None:
            if self._alerts is None:
                self._alerts = Alerts(None)
        else:
            if len(user_json["pools"]) < self._cfg.pool_id:
                if self._alerts is None:
                    self._alerts = Alerts(None)
            else:
                self._alerts = Alerts(user_json["pools"][self._cfg.pool_id - 1])
        return self._alerts

    def get_treatment(self) -> Treatment:
        """Return treatment Detail"""
        user_json = self._connect.get_user_json()
        if user_json is None:
            if self._treatment is None:
                self._treatment = Treatment(None)
        else:
            if len(user_json["pools"]) < self._cfg.pool_id:
                if self._treatment is None:
                    self._treatment = Treatment(None)
            else:
                self._treatment = Treatment(user_json["pools"][self._cfg.pool_id - 1])
        return self._treatment

    def turn_on_module(self, modules, module_id) -> bool:
        """Turn on the specified module, only 1 and 2 are available (0 is pump)"""
        if module_id == 0:
            return False

        module_list = self._connect.get_bpc_modules()
        # Find the module to turn on
        if len(module_list) - 1 < module_id:
            _LOGGER.debug("BPC Module %s doesn't exists", module_id)
            return False

        module = module_list[module_id]
        if module["time"] != "00:00":
            _LOGGER.debug("BPC Module %s already on for %s", module_id, module["time"])
            return True

        status = self._connect.turn_on_light(modules, module_id)
        if status is True:
            _LOGGER.debug("BPC Module %s turning on", module_id)

        return status

    def turn_off_module(self, modules, module_id) -> bool:
        """Turn on the specified module, only 1 and 2 are available (0 is pump)"""
        if module_id == 0:
            return False

        module_list = self._connect.get_bpc_modules()
        # Find the module to turn on
        if len(module_list) - 1 < module_id:
            _LOGGER.debug("BPC Module %s doesn't exists", module_id)
            return False

        module = module_list[module_id]
        if module["time"] == "00:00":
            _LOGGER.debug("BPC Module %s already off", module_id)
            return True

        status = self._connect.turn_off_light(modules, module_id)
        if status is True:
            _LOGGER.debug("BPC Module %s turning off", module_id)

        return True

    def refresh_datas(self) -> None:
        """Refreshing datas"""
        self._connect.easycare_update_user()
        self._connect.easycare_update_modules()
        self._connect.easycare_update_bpc_modules()
