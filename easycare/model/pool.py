"""Class reprsenting pool data"""
import json


class Pool:
    """
    Class representing a pool object
    """

    def __init__(self, pool: json) -> None:
        if pool is None:
            pool = json.loads("{}")
            self._is_filled = False
        else:
            self._is_filled = True
        self._pool = pool

    @property
    def is_filled(self) -> bool:
        """Return True if the client object is filled"""
        return self._is_filled

    @property
    def model(self) -> str:
        """The pool model"""
        return self._pool["model"] if "model" in self._pool else "Unknown"

    @property
    def volume(self) -> float:
        """The pool volume"""
        return float(self._pool["volume"]) if "volume" in self._pool else 0.0

    @property
    def address(self) -> str:
        """The pool address"""
        return self._pool["address"] if "address" in self._pool else ""

    @property
    def latitude(self) -> float:
        """The pool latitude"""
        return float(self._pool["latitude"]) if "latitude" in self._pool else 0.0

    @property
    def longitude(self) -> float:
        """The pool longitude"""
        return float(self._pool["longitude"]) if "longitude" in self._pool else 0.0

    @property
    def custom_photo(self) -> str:
        """The pool custom photo"""
        return self._pool["customPhoto"] if "customPhoto" in self._pool else ""
