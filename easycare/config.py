"""Class used to store all the variable used in the Easy-Care component."""

import logging

_LOGGER = logging.getLogger("custom_components.ha-easycare-waterair")
DEFAULT_HOST = "https://easycare.waterair.com"
UNSET = "unset"


class EasyCareConfig:
    """Helper class to store EasyCare configuration varaibles."""

    def __init__(self, **kwargs) -> None:
        """Initilisation of the class.

        Args:
            kwargs (kwargs): Configuration options.

        """
        self._kw = kwargs

    @property
    def token(self) -> str:
        """The token used for login."""
        return self._kw.get("token") if self._kw.get("token") is not None else UNSET

    @property
    def host(self) -> str:
        """The waterair host."""
        return (
            self._kw.get("host") if self._kw.get("host") is not None else DEFAULT_HOST
        )

    @property
    def pool_id(self) -> int:
        """The waterair host."""
        return (
            int(self._kw.get("pool_id")) if self._kw.get("pool_id") is not None else 1
        )

    @property
    def unset(self) -> str:
        """The unset value."""
        return UNSET
