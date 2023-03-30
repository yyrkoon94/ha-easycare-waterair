"""Class reprsenting client data"""
import json


class Client:
    """
    Class representing a client object
    """

    def __init__(self, client: json) -> None:
        if client is None:
            client = json.loads("{}")
            self._is_filled = False
        else:
            self._is_filled = True
        self._client = client

    @property
    def is_filled(self) -> bool:
        """Return True if the client object is filled"""
        return self._is_filled

    @property
    def first_name(self) -> str:
        """The client first name"""
        return self._client["firstName"] if "firstName" in self._client else "Unknown"

    @property
    def last_name(self) -> str:
        """The client last name"""
        return self._client["lastName"] if "lastName" in self._client else "Unknown"

    @property
    def address_line1(self) -> str:
        """The client adress first line"""
        return self._client["addressLine1"] if "addressLine1" in self._client else ""

    @property
    def address_line2(self) -> str:
        """The client adress second line"""
        return self._client["addressLine2"] if "addressLine2" in self._client else ""

    @property
    def postal_code(self) -> str:
        """The client postal code"""
        return self._client["postalCode"] if "postalCode" in self._client else ""

    @property
    def city(self) -> str:
        """The client city"""
        return self._client["city"] if "city" in self._client else ""

    @property
    def email(self) -> str:
        """The client postal code"""
        return self._client["email"] if "email" in self._client else ""
