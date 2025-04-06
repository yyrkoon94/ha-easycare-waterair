"""Class reprsenting client data."""

import json


class Client:
    """Class representing a client object."""

    def __init__(self, client: json) -> None:
        """Initilisation of the class."""
        if client is None:
            client = json.loads("{}")
            self._is_filled = False
        else:
            self._is_filled = True
        self._client = client

    @property
    def is_filled(self) -> bool:
        """Return True if the client object is filled."""
        return self._is_filled

    @property
    def first_name(self) -> str:
        """Return the client first name."""
        return self._client.get("firstName", "Unknown")

    @property
    def last_name(self) -> str:
        """Return the client last name."""
        return self._client.get("lastName", "Unknown")

    @property
    def address_line1(self) -> str:
        """Return the client adress first line."""
        return self._client.get("addressLine1", "")

    @property
    def address_line2(self) -> str:
        """Return the client adress second line."""
        return self._client.get("addressLine2", "")

    @property
    def postal_code(self) -> str:
        """Return the client postal code."""
        return self._client.get("postalCode", "")

    @property
    def city(self) -> str:
        """Return the client city."""
        return self._client.get("city", "")

    @property
    def email(self) -> str:
        """Return the client postal code."""
        return self._client.get("email", "")
