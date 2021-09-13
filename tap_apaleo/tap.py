"""Apaleo tap class."""

from typing import List

from singer_sdk import Tap, Stream
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_apaleo.streams import (
    ReservationsStream,
    PropertiesStream,
    UnitGroupsStream,
    UnitsStream
)

STREAM_TYPES = [
    ReservationsStream,
    PropertiesStream,
    UnitGroupsStream,
    UnitsStream
]


class TapApaleo(Tap):
    """Apaleo tap class."""
    name = "tap-apaleo"

    config_jsonschema = th.PropertiesList(
        th.Property("client_id", th.StringType, required=True),
        th.Property("client_secret", th.StringType, required=True),
        th.Property("start_date", th.DateTimeType, required=True),
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]
