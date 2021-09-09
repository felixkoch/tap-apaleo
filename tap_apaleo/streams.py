"""Stream type classes for tap-apaleo."""

from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_apaleo.client import ApaleoStream

from singer_sdk.typing import (
    ArrayType,
    BooleanType,
    DateTimeType,
    IntegerType,
    NumberType,
    ObjectType,
    PropertiesList,
    Property,
    StringType,
)



SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")



class PropertiesStream(ApaleoStream):
    """Define custom stream."""
    name = "properties"
    path = "/inventory/v1/properties"
    primary_keys = ["id"]
    replication_key = None
    records_jsonpath = "$.properties[*]"

    #schema_filepath = SCHEMAS_DIR / "properties.json"

    schema = PropertiesList(
        Property("id", StringType),
        Property("code", StringType),
        Property("propertyTemplateId", StringType),
        Property("isTemplate", BooleanType),
        Property("name", StringType),
        Property("description", StringType),
        Property("companyName", StringType),
        Property("managingDirectors", StringType),
        Property("commercialRegisterEntry", StringType),
        Property("taxId", StringType),
        Property("location", ObjectType(
            Property("addressLine1", StringType),
            Property("", StringType),
            Property("addressLine2", StringType),
            Property("postalCode", StringType),
            Property("city", StringType),
            Property("regionCode", StringType),
            Property("countryCode", StringType)

        )),
        Property("bankAccount", ObjectType(
            Property("iban", StringType),
            Property("bic", StringType),
            Property("bank", StringType)
        )),
        Property("paymentTerms", ObjectType(
            Property("en", StringType)
        )),
        Property("timeZone", StringType),
        Property("currencyCode", StringType),
        Property("created",  DateTimeType),
        Property("status", StringType),
        Property("isArchived", BooleanType),
    ).to_dict()




class ReservationsStream(ApaleoStream):
    """Define custom stream."""
    name = "reservations"
    path = "/booking/v1/reservations"
    primary_keys = ["id"]
    replication_key = "modified"
    records_jsonpath = "$.reservations[*]"

    schema_filepath = SCHEMAS_DIR / "reservations.json"


