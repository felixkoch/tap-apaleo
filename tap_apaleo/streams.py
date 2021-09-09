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

API_DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

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

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        self.logger.info("############################ get_url_params() ############################")
        starting_timestamp = self.get_starting_timestamp(context)
        self.logger.info(starting_timestamp)

        self.logger.info(next_page_token)
        params: dict = {}
        params["pageSize"] = 1000
        if next_page_token:
            params["page"] = next_page_token

        params['expand'] = 'timeSlices'
        params['dateFilter'] = 'Modification'
        params['from'] = starting_timestamp.strftime(API_DATE_FORMAT)
        params["sort"] = 'updated:asc'

        self.logger.info(params)    
        return params


