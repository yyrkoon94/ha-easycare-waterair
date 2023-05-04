"""Class representing module object"""
import json


class Module:
    """
    Class representing the module object
    """

    def __init__(self, module: json) -> None:
        if module is None:
            module = json.loads("{}")
            self._is_filled = False
        else:
            self._is_filled = True

        self._type = module["type"]
        self._name = module["name"]
        self._id = module["id"]
        self._serial_number = module["serialNumber"]
        self._image = module["customPhoto"]

    @property
    def is_filled(self) -> bool:
        """Return True if the module object is filled"""
        return self._is_filled

    @property
    def type(self) -> str:
        """The module type"""
        return self._type

    @property
    def name(self) -> str:
        """The module name"""
        return self._name

    @property
    def id(self) -> str:
        """The module id"""
        return self._id

    @property
    def serial_number(self) -> str:
        """The module name"""
        return self._serial_number

    @property
    def image(self) -> str:
        """The module name"""
        return self._image
