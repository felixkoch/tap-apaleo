"""Stream type classes for tap-apaleo."""

from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_apaleo.client import ApaleoStream


SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")



class PropertiesStream(ApaleoStream):
    """Define custom stream."""
    name = "properties"
    path = "/inventory/v1/properties"
    primary_keys = ["id"]
    replication_key = None
    records_jsonpath = "$.properties[*]"

    schema_filepath = SCHEMAS_DIR / "properties.json"



class ReservationsStream(ApaleoStream):
    """Define custom stream."""
    name = "reservations"
    path = "/booking/v1/reservations"
    primary_keys = ["id"]
    replication_key = "modified"
    records_jsonpath = "$.reservations[*]"

    schema_filepath = SCHEMAS_DIR / "reservations.json"


