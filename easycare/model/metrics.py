"""Class reprsenting pool data."""

from datetime import datetime
import json

from dateutil import parser


class Metrics:
    """Class representing the pool metrics."""

    def __init__(self, pool: json) -> None:
        """Initilisation of the class."""
        if pool is None:
            pool = json.loads("{}")
            self._is_filled = False
        else:
            self._is_filled = True
        self._pool = pool

        if "status" in pool:
            if "lastPhMeasure" in pool["status"]:
                date_ph = (
                    datetime.fromtimestamp(pool["status"]["lastPhMeasure"]["date"])
                    if "date" in pool["status"]["lastPhMeasure"]
                    else parser.parse(pool["status"]["lastPhMeasure"]["timestamp"])
                )
                self._last_ph_measure = {
                    "value": pool["status"]["lastPhMeasure"]["value"],
                    "date": date_ph,
                }
            if "lastRedoxMeasure" in pool["status"]:
                date_chlorine = (
                    datetime.fromtimestamp(pool["status"]["lastRedoxMeasure"]["date"])
                    if "date" in pool["status"]["lastRedoxMeasure"]
                    else parser.parse(pool["status"]["lastRedoxMeasure"]["timestamp"])
                )
                self._last_chlorine_measure = {
                    "value": pool["status"]["lastRedoxMeasure"]["value"],
                    "date": date_chlorine,
                }
            if "lastTemperatureMeasure" in pool["status"]:
                date_temperature = (
                    datetime.fromtimestamp(
                        pool["status"]["lastTemperatureMeasure"]["date"]
                    )
                    if "date" in pool["status"]["lastTemperatureMeasure"]
                    else parser.parse(
                        pool["status"]["lastTemperatureMeasure"]["timestamp"]
                    )
                )
                self._last_temperature_measure = {
                    "value": pool["status"]["lastTemperatureMeasure"]["value"],
                    "date": date_temperature,
                }
            if "lastPressureMeasure" in pool["status"]:
                date_pressure = (
                    datetime.fromtimestamp(
                        pool["status"]["lastPressureMeasure"]["date"]
                    )
                    if "date" in pool["status"]["lastPressureMeasure"]
                    else parser.parse(
                        pool["status"]["lastPressureMeasure"]["timestamp"]
                    )
                )
                self._last_pressure_measure = {
                    "value": pool["status"]["lastPressureMeasure"]["value"],
                    "date": date_pressure,
                }

    @property
    def is_filled(self) -> bool:
        """Return True if the client object is filled."""
        return self._is_filled

    @property
    def last_ph_measure_value(self) -> str:
        """The ph value."""
        return self._last_ph_measure.get("value", "Unknown")

    @property
    def last_ph_measure_date(self) -> str:
        """The ph date."""
        return self._last_ph_measure.get("date", "Unknown")

    @property
    def last_chlorine_measure_value(self) -> str:
        """The chlorine value."""
        return self._last_chlorine_measure.get("value", "Unknown")

    @property
    def last_chlorine_measure_date(self) -> str:
        """The chlorine date."""
        return self._last_chlorine_measure.get("date", "Unknown")

    @property
    def last_temperature_measure_value(self) -> str:
        """The temperature value."""
        return self._last_temperature_measure.get("value", "Unknown")

    @property
    def last_temperature_measure_date(self) -> str:
        """The temperature date."""
        return self._last_temperature_measure.get("date", "Unknown")

    @property
    def last_pressure_measure_value(self) -> str:
        """The pressure value."""
        return self._last_pressure_measure.get("value", "Unknown")

    @property
    def last_pressure_measure_date(self) -> str:
        """The pressure date."""
        return self._last_pressure_measure.get("date", "Unknown")
