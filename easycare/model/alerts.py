"""Class reprsenting pool data."""

import json

from dateutil import parser


class Alerts:
    """Class representing the pool alerts."""

    def __init__(self, pool: json) -> None:
        """Initilisation of the class."""
        if pool is None:
            pool = json.loads("{}")
            self._is_filled = False
        else:
            self._is_filled = True
        self._pool = pool
        self._notifications = []
        if "notifications" in pool:
            if pool["notifications"] != {}:
                for notification in pool["notifications"]:
                    date_notification = parser.parse(
                        pool["notifications"][notification]["date"]
                    )
                    self._notifications.append(
                        {
                            "value": pool["notifications"][notification]["action"],
                            "date": date_notification,
                        }
                    )

    @property
    def is_filled(self) -> bool:
        """Return True if the client object is filled."""
        return self._is_filled

    @property
    def notification_size(self) -> int:
        """Get the number of notifications."""
        return len(self._notifications)

    def notification_value(self, notification_id) -> str:
        """Get the notification value."""
        return (
            self._notifications[notification_id]["value"]
            if len(self._notifications) > 0
            and "value" in self._notifications[notification_id]
            else "None"
        )

    def notification_date(self, notification_id) -> str:
        """Get the notification date."""
        return (
            self._notifications[notification_id]["date"]
            if len(self._notifications) > 0
            and "date" in self._notifications[notification_id]
            else None
        )
