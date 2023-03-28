"""
    This class is used to store all the variable used in the Easy-Care component
"""
import logging

_LOGGER = logging.getLogger("custom_components.ha-easycare-waterair")
DEFAULT_HOST = "https://easycare.waterair.com"
UNSET = "unset"


class EasyCareConfig:
    """Helper class to store EasyCare configuration varaibles."""

    def __init__(self, **kwargs) -> None:
        """The constructor.

        Args:
            kwargs (kwargs): Configuration options.

        """
        self._kw = kwargs
        _LOGGER.debug("EasyCare starting configuration")

    @property
    def username(self) -> str:
        """The username used for login"""
        return self._kw.get("username", UNSET)

    @property
    def password(self) -> str:
        """The password used for login"""
        return self._kw.get("password", UNSET)

    @property
    def easycare_key(self) -> str:
        """The api key"""
        return self._kw.get("easycare_key", UNSET)

    @property
    def host(self) -> str:
        """The waterair host"""
        return self._kw.get("host", DEFAULT_HOST)

    @property
    def unset(self) -> str:
        """The unset value"""
        return UNSET
