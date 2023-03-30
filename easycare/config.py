"""
    This class is used to store all the variable used in the Easy-Care component
"""
import logging

_LOGGER = logging.getLogger("custom_components.ha-easycare-waterair")
DEFAULT_HOST = "https://easycare.waterair.com"
EASYCARE_KEY = "NWQwMjFkYzI0NzhjMjE3MDc3MzI0NDEwOkNtVmZxNDNiZE5hUUZjWA=="
UNSET = "unset"


class EasyCareConfig:
    """Helper class to store EasyCare configuration varaibles."""

    def __init__(self, **kwargs) -> None:
        """The constructor.

        Args:
            kwargs (kwargs): Configuration options.

        """
        self._kw = kwargs

    @property
    def username(self) -> str:
        """The username used for login"""
        return (
            self._kw.get("username") if self._kw.get("username") is not None else UNSET
        )

    @property
    def password(self) -> str:
        """The password used for login"""
        return (
            self._kw.get("password") if self._kw.get("password") is not None else UNSET
        )

    @property
    def easycare_key(self) -> str:
        """The api key"""
        return (
            self._kw.get("easycare_key")
            if self._kw.get("easycare_key") is not None
            else EASYCARE_KEY
        )

    @property
    def host(self) -> str:
        """The waterair host"""
        return (
            self._kw.get("host") if self._kw.get("host") is not None else DEFAULT_HOST
        )

    @property
    def pool_id(self) -> int:
        """The waterair host"""
        return (
            int(self._kw.get("pool_id")) if self._kw.get("pool_id") is not None else 1
        )

    @property
    def unset(self) -> str:
        """The unset value"""
        return UNSET
