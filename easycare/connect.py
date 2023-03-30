"""
    This class is used to manage all calls to Easy-Care API
"""
import logging
import json
import requests
import time
from .config import EasyCareConfig

_LOGGER = logging.getLogger("custom_components.ha-easycare-waterair")
TEMP_BEARER = "QESosTRAltaiHhBFfIMi35flqeiH1O32ZFWqnj6FTVGEUeRzhlckS5dg3STITccefk9uEy7e9YWVKwJ2dgq7W4XLmuwVbMAOi61U2OYlYvakOdo1EJ1RCJriAad7hIQID2mUgqfF75TUmktAg2FpfYcTFOnTLSfTuAxtCvFPnYiaGzmO7eJsFTtU0YltUlWBNns8RBOizQEMOAUdRSCCWHI0z4qpvvouR97nAt0x7c1GaVqhhWB1TeAi1JUwkcLB"


class Connect:
    """Class is used to manage all calls to Easy-Care API."""

    def __init__(self, config: EasyCareConfig) -> None:
        """The constructor.

        Args:
            config (EasyCareConfig): Configuration variables.

        """
        self._config = config
        self._bearer = TEMP_BEARER  # None
        self._bearer_timeout = 0  # time.time()
        # self._bearer = None
        # self._bearer_timeout = time.time()
        self._is_connected = False

    def login(self) -> bool:
        """Login to Easy-Care and Store the Bearer"""
        if self.check_bearer() is True:
            _LOGGER.debug("Bearer is defined, no need to login !")
            self._is_connected = True
            return True

        _LOGGER.debug("Bearer is expired or not set, calling login api")
        user = self._easycare_login()
        if user is False:
            self._is_connected = False
            return False

        self._bearer = user["access_token"]
        self._bearer_timeout = time.time() + user["expires_in"]
        self._is_connected = True
        return True

    def check_bearer(self) -> bool:
        """Check if Bearer is always valid"""
        if time.time() > self._bearer_timeout and self._bearer_timeout != 0:
            self._bearer = None

        return self._bearer is not None

    def _easycare_login(self) -> json:
        """Login to Easy-Care plateform"""
        if (
            self._config.username == self._config.unset
            or self._config.password == self._config.unset
        ):
            return False

        headers = {
            "Content-Type": "application/json",
            "User-Agent": "connected-pool-waterair/2.4.6 (iPad; iOS 16.3; Scale/2.00)",
            "authorization": "Basic " + self._config.easycare_key,
            "accept": "version=2.5",
        }

        attempt = 0
        login = None
        while attempt < 1:
            attempt += 1
            _LOGGER.debug("Login attempt #%s", attempt)
            login = requests.post(
                self._config.host + "/oauth2/token",
                json={
                    "scope": "email",
                    "password": self._config.password,
                    "username": self._config.username,
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
            _LOGGER.error("Authentication failed !")
            return False
        if login.status_code != 200:
            _LOGGER.error(
                "Request failed, status_code is %s and message %s",
                login.status_code,
                login.content,
            )
            return False

        _LOGGER.debug("Authentication done !")
        return json.loads(login.content)

    def get_connection_status(self) -> bool:
        """Return the connextion status for Easy-Care"""
        return self._is_connected

    def easycare_get_user(self) -> json:
        """Get User detail by calling getUser"""
        if self._is_connected is False:
            self._easycare_login()

        if self._is_connected is False:
            return None

        headers = {
            "Content-Type": "application/json",
            "User-Agent": "connected-pool-waterair/2.4.6 (iPad; iOS 16.3; Scale/2.00)",
            "authorization": "Bearer " + self._bearer,
            "accept": "version=2.5",
        }

        attempt = 0
        user = None
        while attempt < 1:
            attempt += 1
            _LOGGER.debug("GetUser attempt #%s", attempt)
            user = requests.post(
                self._config.host + "/api/getUser?attributesToPopulate%5B%5D=pools",
                headers=headers,
                timeout=3,
                verify=False,
            )
            if user is not None:
                break
            time.sleep(1)
        if user is None:
            _LOGGER.error("Error calling getUser")
            self._is_connected = False
            return None
        if user.status_code != 200:
            _LOGGER.error(
                "Request failed, status_code is %s and message %s",
                user.status_code,
                user.content,
            )
            self._is_connected = False
            return None

        _LOGGER.debug("GetUser done !")
        return json.loads(user.content)
