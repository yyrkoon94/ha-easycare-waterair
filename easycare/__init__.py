import logging
from .config import EasyCareConfig
from .connect import Connect

_LOGGER = logging.getLogger("custom_components.ha-easycare-waterair")


class EasyCare:
    """Entry point for all Easy-Care operations."""

    def __init__(self, **kwargs) -> None:
        """Constructor for the Easy-Care object."""
        _LOGGER.debug("EasyCare component initialisation")

        # Set up the config first.
        self._cfg = EasyCareConfig(**kwargs)
        self._connect = Connect(self._cfg)

    def connect(self) -> bool:
        """Call the connect api for the first login"""
        return self._connect.login()

    def connecton_status(self) -> bool:
        """Return the connextion status for Easy-Care"""
        return self._connect.connecton_status()
