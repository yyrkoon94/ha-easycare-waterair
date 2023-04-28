"""Class reprsenting pool data"""
import json
from datetime import datetime


class Metrics:
    """
    Class representing the pool metrics
    """

    def __init__(self, pool: json) -> None:
        if pool is None:
            pool = json.loads("{}")
            self._is_filled = False
        else:
            self._is_filled = True
        self._pool = pool

        if "status" in pool:
            if "lastPhMeasure" in pool["status"]:
                date_ph = datetime.fromtimestamp(
                    pool["status"]["lastPhMeasure"]["date"]
                )
                self._last_ph_measure = {
                    "value": pool["status"]["lastPhMeasure"]["value"],
                    "date": date_ph,
                }
            if "lastRedoxMeasure" in pool["status"]:
                date_chlorine = datetime.fromtimestamp(
                    pool["status"]["lastRedoxMeasure"]["date"]
                )
                self._last_chlorine_measure = {
                    "value": pool["status"]["lastRedoxMeasure"]["value"],
                    "date": date_chlorine,
                }
            if "lastTemperatureMeasure" in pool["status"]:
                date_temperature = datetime.fromtimestamp(
                    pool["status"]["lastTemperatureMeasure"]["date"]
                )
                self._last_temperature_measure = {
                    "value": pool["status"]["lastTemperatureMeasure"]["value"],
                    "date": date_temperature,
                }

    @property
    def is_filled(self) -> bool:
        """Return True if the client object is filled"""
        return self._is_filled

    @property
    def last_ph_measure_value(self) -> str:
        """The ph value"""
        return (
            self._last_ph_measure["value"]
            if "value" in self._last_ph_measure
            else "Unknown"
        )

    @property
    def last_ph_measure_date(self) -> str:
        """The ph value"""
        return (
            self._last_ph_measure["date"]
            if "date" in self._last_ph_measure
            else "Unknown"
        )

    @property
    def last_chlorine_measure_value(self) -> str:
        """The ph value"""
        return (
            self._last_chlorine_measure["value"]
            if "value" in self._last_chlorine_measure
            else "Unknown"
        )

    @property
    def last_chlorine_measure_date(self) -> str:
        """The ph value"""
        return (
            self._last_chlorine_measure["date"]
            if "date" in self._last_chlorine_measure
            else "Unknown"
        )

    @property
    def last_temperature_measure_value(self) -> str:
        """The ph value"""
        return (
            self._last_temperature_measure["value"]
            if "value" in self._last_temperature_measure
            else "Unknown"
        )

    @property
    def last_temperature_measure_date(self) -> str:
        """The ph value"""
        return (
            self._last_temperature_measure["date"]
            if "date" in self._last_temperature_measure
            else "Unknown"
        )
