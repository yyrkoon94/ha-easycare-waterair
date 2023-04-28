"""Class reprsenting pool data"""
import json
from datetime import datetime


class Alerts:
    """
    Class representing the pool alerts
    """

    def __init__(self, pool: json) -> None:
        if pool is None:
            pool = json.loads("{}")
            self._is_filled = False
        else:
            self._is_filled = True
        self._pool = pool

        if "notifications" in pool:
            for notification in pool["notifications"]:
                date_notification = datetime.fromisoformat(
                    pool["notifications"][notification]["date"]
                )
                self._notification = {
                    "value": pool["notifications"][notification]["action"],
                    "date": date_notification,
                }
                break

    @property
    def is_filled(self) -> bool:
        """Return True if the client object is filled"""
        return self._is_filled

    @property
    def notification_value(self) -> str:
        """The notification value"""
        return (
            self._notification["value"] if "value" in self._notification else "Unknown"
        )

    @property
    def notification_date(self) -> str:
        """The notification date"""
        return self._notification["date"] if "date" in self._notification else "Unknown"
