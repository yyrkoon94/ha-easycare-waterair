"""Class reprsenting pool data"""
import json
from dateutil import parser


class Treatment:
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

        if "waterChemistryCorrectionProtocol" in pool:
            if pool["waterChemistryCorrectionProtocol"] is not None:
                date_treatment = parser.parse(
                    pool["waterChemistryCorrectionProtocol"][
                        "lastPHOutOfControlAlertSentDate"
                    ]
                )
                self._treatment = {
                    "value": pool["waterChemistryCorrectionProtocol"][
                        "correctionProtocolType"
                    ],
                    "date": date_treatment,
                }
            else:
                self._treatment = {}
        else:
            self._treatment = {}

    @property
    def is_filled(self) -> bool:
        """Return True if the client object is filled"""
        return self._is_filled

    @property
    def treatment_value(self) -> str:
        """The notification value"""
        return self._treatment["value"] if "value" in self._treatment else "None"

    @property
    def treatment_date(self) -> str:
        """The notification date"""
        return self._treatment["date"] if "date" in self._treatment else None
