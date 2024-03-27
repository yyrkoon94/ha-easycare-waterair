"""
    This class is used to manage all calls to Easy-Care API
"""
from homeassistant.core import HomeAssistant
import logging
import json
import requests
import time
import os.path
from .config import EasyCareConfig

_LOGGER = logging.getLogger("custom_components.ha-easycare-waterair")

bearerstore = "/custom_components/ha-easycare-waterair/.easycarebearer"

class Connect:
    """Class is used to manage all calls to Easy-Care API."""

    def __init__(self, config: EasyCareConfig, hass: HomeAssistant) -> None:
        """The constructor.

        Args:
            config (EasyCareConfig): Configuration variables.

        """
        self._hass = hass
        self._config = config
        self._bearer_timeout = -1
        self._bearer = None
        self._is_connected = False
        self._user_json = None
        self._modules = None
        self._bpc_modules = None
        self._call_light_change = False

    def login(self) -> bool:
        """Login to Easy-Care and Store the Bearer"""

        if self._check_bearer() is True:
            _LOGGER.debug("Bearer is defined, no need to login !")
            self._is_connected = True
            return True

        if os.path.isfile(bearerstore) is True:
            _LOGGER.debug("Bearer is store in file, try to read it")
            f = open(bearerstore, "r")
            self._bearer = f.readline().strip()
            if self._bearer == "":
                self._bearer = None
            self._bearer_timeout = f.readline().strip()
            if self._bearer_timeout != "":
                self._bearer_timeout = float(self._bearer_timeout)
            else:
                self._bearer_timeout = -1
            f.close()
            if self._check_bearer() is True:
                _LOGGER.debug("Bearer is defined in file, no need to login !")
                self._is_connected = True
                return True
        else:
            f = open(bearerstore, "x")
            f.close()

        _LOGGER.debug("Bearer is expired or not set, calling login api")
        user = self._easycare_login()
        if user is False:
            self._is_connected = False
            return False

        self._bearer = user["access_token"]
        self._bearer_timeout = time.time() + user["expires_in"]
        self._is_connected = True
        if os.path.isfile(bearerstore) is True:
            f = open(bearerstore, "w")
            f.write(self._bearer)
            f.write("\n")
            f.write(str(self._bearer_timeout))
            f.close()

        return True

    def reset_bearer(self) -> None:
        self._bearer = None
        self._bearer_timeout = None
        if os.path.isfile(bearerstore) is True:
            os.remove(bearerstore)

    def _check_bearer(self) -> bool:
        """Check if Bearer is always valid"""
        if self._bearer is None:
            return None
        if time.time() > self._bearer_timeout and self._bearer_timeout != 0:
            self._bearer = None

        return self._bearer is not None

    def _easycare_login(self) -> json:
        """Login to Easy-Care plateform"""
        if (
            self._config.token == self._config.unset
        ):
            return False

        params = {
            "code": self._config.token,
            "grant_type": "authorization_code",
            "code_verifier": "w-j6efyTpo1umXD0hFZPRM8l7kD9yScwZ3E5rAHJuE4"
        }

        attempt = 0
        login = None
        while attempt < 1:
            attempt += 1
            _LOGGER.debug("Get acces_token attempt #%s", attempt)
            login = requests.post(
                "https://sso.waterair.com/waterairexternb2c.onmicrosoft.com/b2c_1a_signup_signin_inter/oauth2/v2.0/token",
                params=params,
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

        _LOGGER.debug("Get the access token done !")
        access_token = json.loads(login.content)["id_token"]

        headers = {
            "authorization": "Basic NWQwMjFkYzI0NzhjMjE3MDc3MzI0NDEwOkNtVmZxNDNiZE5hUUZjWA==",
        }
        attempt = 0
        login = None
        while attempt < 1:
            attempt += 1
            _LOGGER.debug("Get bearer attempt #%s", attempt)
            login = requests.post(
                self._config.host + "/oauth2/tokenFromAzureADB2CIdToken",
                json={
                    "idToken": access_token,
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

        _LOGGER.debug("Get the bearer done !")

        return json.loads(login.content)

    def get_connection_status(self) -> bool:
        """Return the connextion status for Easy-Care"""
        return self._is_connected

    def get_user_json(self) -> json:
        """Return the user json for Easy-Care"""
        return self._user_json

    def get_modules(self) -> json:
        """Return the modules for Easy-Care"""
        if self._modules is not None:
            return self._modules

        self.easycare_update_modules()
        return self._modules

    def get_bpc_modules(self) -> json:
        """Return the modules for Easy-Care"""
        if self._bpc_modules is not None:
            return self._bpc_modules

        self.easycare_update_bpc_modules()
        return self._bpc_modules

    def easycare_update_modules(self) -> None:
        """Get modules detail by calling getUserWithHisModules"""
        if self._is_connected is False:
            self.login()

        if self._is_connected is False:
            return None

        headers = {
            "Content-Type": "application/json",
            "User-Agent": "connected-pool-waterair/2.4.6 (iPad; iOS 16.3; Scale/2.00)",
            "authorization": "Bearer " + self._bearer,
            "accept": "version=2.5",
        }

        attempt = 0
        modules = None
        while attempt < 1:
            attempt += 1
            _LOGGER.debug("getUserWithHisModules attempt #%s", attempt)
            modules = requests.get(
                self._config.host + "/api/getUserWithHisModules",
                headers=headers,
                timeout=3,
                verify=False,
            )
            if modules is not None:
                break
            time.sleep(1)
        if modules is None:
            _LOGGER.error("Error calling getUserWithHisModules")
            return None
        if modules.status_code != 200:
            _LOGGER.error(
                "Request failed, status_code is %s and message %s",
                modules.status_code,
                modules.content,
            )
            return None
        json_modules = json.loads(modules.content)
        self._modules = json_modules["modules"]
        _LOGGER.debug("getUserWithHisModules done !")

    def easycare_update_user(self) -> None:
        """Get User detail by calling getUser"""
        if self._is_connected is False:
            self.login()

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
            user = requests.get(
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

        self._user_json = json.loads(user.content)
        _LOGGER.debug("GetUser done !")

    def easycare_update_bpc_modules(self) -> None:
        """Return the modules for Easy-Care"""
        if self._call_light_change is True:
            return None

        if self._is_connected is False:
            self.login()

        if self._is_connected is False:
            return None

        watbox_serial_number = None
        bpc_name = None

        for module in self._modules:
            if module["type"] == "lr-bst-compact":
                watbox_serial_number = module["serialNumber"]
            if module["type"] == "lr-pc":
                bpc_name = module["name"][4::]

        headers = {
            "Content-Type": "application/json",
            "User-Agent": "connected-pool-waterair/2.4.6 (iPad; iOS 16.3; Scale/2.00)",
            "authorization": "Bearer " + self._bearer,
            "accept": "version=2.5",
        }

        attempt = 0
        bpc_modules = None
        while attempt < 1:
            attempt += 1
            _LOGGER.debug("getBPCModules attempt #%s", attempt)
            bpc_modules = requests.get(
                self._config.host
                + "/api/module/"
                + watbox_serial_number
                + "/status/"
                + bpc_name,
                headers=headers,
                timeout=3,
                verify=False,
            )
            if bpc_modules is not None:
                break
            time.sleep(1)
        if bpc_modules is None:
            _LOGGER.error("Error calling getBPCModules")
            return None
        if bpc_modules.status_code != 200:
            _LOGGER.error(
                "Request failed, status_code is %s and message %s",
                bpc_modules.status_code,
                bpc_modules.content,
            )
            return None
        json_modules = json.loads(bpc_modules.content)
        self._bpc_modules = json_modules["pool"]
        _LOGGER.debug("getBPCModules done !")

    def turn_on_light(self, modules, light_id) -> bool:
        """Turn on the light"""
        duration = 3600
        if light_id == 1:
            # Spot duration
            number = self._hass.states.get(
                "number.easy_care_pool_spot_light_duration_in_hours"
            )
            if number is not None:
                duration = int(float(number.state)) * 3600
        if light_id == 2:
            # Spot duration
            number = self._hass.states.get(
                "number.easy_care_pool_escalight_light_duration_in_hours"
            )
            if number is not None:
                duration = int(float(number.state)) * 3600

        if modules is None:
            return False

        if self._is_connected is False:
            self.login()

        if self._is_connected is False:
            return False

        watbox_serial_number = None
        bpc_name = None
        bpc_id = None
        self._call_light_change = True
        for module in modules:
            if module.type == "lr-bst-compact":
                watbox_serial_number = module.serial_number
            if module.type == "lr-pc":
                bpc_name = module.name[4::]
                bpc_id = module.id

        headers = {
            "Content-Type": "application/json",
            "User-Agent": "connected-pool-waterair/2.4.6 (iPad; iOS 16.3; Scale/2.00)",
            "authorization": "Bearer " + self._bearer,
            "accept": "version=2.5",
        }

        body = {"pool": {"index": light_id, "manualDuration": duration, "action": 2}}

        confirm_body = {
            "command": {
                "pool": {"manualDuration": duration, "index": light_id, "action": 2}
            },
            "route": "http",
            "id": bpc_id,
        }

        attempt = 0
        result = None
        while attempt < 1:
            attempt += 1
            _LOGGER.debug("TurnOnLight attempt #%s", attempt)
            result = requests.post(
                self._config.host
                + "/api/module/"
                + watbox_serial_number
                + "/manual/"
                + bpc_name,
                headers=headers,
                json=body,
                timeout=3,
                verify=False,
            )
            if result is not None:
                break
            time.sleep(1)
        if result is None:
            _LOGGER.error("Error calling TurnOnLight")
            self._call_light_change = False
            return False
        if result.status_code != 200:
            _LOGGER.error(
                "Request failed, status_code is %s and message %s",
                result.status_code,
                result.content,
            )
            self._call_light_change = False
            return False

        # Now call confirmation
        attempt = 0
        result = None
        while attempt < 1:
            attempt += 1
            _LOGGER.debug("ConfirmationCall attempt #%s", attempt)
            result = requests.post(
                self._config.host + "/api/reportManualCommandSent",
                headers=headers,
                json=confirm_body,
                timeout=3,
                verify=False,
            )
            if result is not None:
                break
            time.sleep(1)
        if result is None:
            _LOGGER.error("Error calling ConfirmationCall")
            self._call_light_change = False
            return False
        if result.status_code != 200:
            _LOGGER.error(
                "Request failed, status_code is %s and message %s",
                result.status_code,
                result.content,
            )
            self._call_light_change = False
            return False

        self.easycare_update_bpc_modules()
        _LOGGER.debug("turnOnLight done !")
        self._bpc_modules = None
        self._call_light_change = False
        return True

    def turn_off_light(self, modules, light_id) -> bool:
        """Turn on the light"""
        if modules is None:
            return False

        if self._is_connected is False:
            self.login()

        if self._is_connected is False:
            return False

        watbox_serial_number = None
        bpc_name = None
        bpc_id = None
        self._call_light_change = True

        for module in modules:
            if module.type == "lr-bst-compact":
                watbox_serial_number = module.serial_number
            if module.type == "lr-pc":
                bpc_name = module.name[4::]
                bpc_id = module.id

        headers = {
            "Content-Type": "application/json",
            "User-Agent": "connected-pool-waterair/2.4.6 (iPad; iOS 16.3; Scale/2.00)",
            "authorization": "Bearer " + self._bearer,
            "accept": "version=2.5",
        }

        body = {"pool": {"index": light_id, "action": 1}}

        confirm_body = {
            "command": {"pool": {"index": light_id, "action": 1}},
            "route": "http",
            "id": bpc_id,
        }

        attempt = 0
        result = None
        while attempt < 1:
            attempt += 1
            _LOGGER.debug("TurnOffLight attempt #%s", attempt)
            result = requests.post(
                self._config.host
                + "/api/module/"
                + watbox_serial_number
                + "/manual/"
                + bpc_name,
                headers=headers,
                json=body,
                timeout=3,
                verify=False,
            )
            if result is not None:
                break
            time.sleep(1)
        if result is None:
            _LOGGER.error("Error calling TurnOffLight")
            self._call_light_change = False
            return False
        if result.status_code != 200:
            _LOGGER.error(
                "Request failed, status_code is %s and message %s",
                result.status_code,
                result.content,
            )
            self._call_light_change = False
            return False

        # Now call confirmation
        attempt = 0
        result = None
        while attempt < 1:
            attempt += 1
            _LOGGER.debug("ConfirmationCall attempt #%s", attempt)
            result = requests.post(
                self._config.host + "/api/reportManualCommandSent",
                headers=headers,
                json=confirm_body,
                timeout=3,
                verify=False,
            )
            if result is not None:
                break
            time.sleep(1)
        if result is None:
            _LOGGER.error("Error calling ConfirmationCall")
            self._call_light_change = False
            return False
        if result.status_code != 200:
            _LOGGER.error(
                "Request failed, status_code is %s and message %s",
                result.status_code,
                result.content,
            )
            self._call_light_change = False
            return False

        self.easycare_update_bpc_modules()
        _LOGGER.debug("TurnOffLight done !")
        self._bpc_modules = None
        self._call_light_change = False
        return True
