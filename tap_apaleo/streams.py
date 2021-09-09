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

API_DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

class PropertiesStream(ApaleoStream):
    """Define custom stream."""
    name = "properties"
    path = "/inventory/v1/properties"
    primary_keys = ["id"]
    replication_key = None
    records_jsonpath = "$.properties[*]"

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

    schema = PropertiesList(
        Property("id", StringType),
        Property("bookingId", StringType),
        Property("blockId", StringType),
        Property("groupName", StringType),
        Property("status", StringType),
        Property("checkInTime", DateTimeType),
        Property("checkOutTime", DateTimeType),
        Property("cancellationTime", DateTimeType),
        Property("noShowTime", DateTimeType),
        Property("property", ObjectType(
            Property("id", StringType),
            Property("code", StringType),
            Property("code", StringType),
            Property("description", StringType),
        )),
        Property("ratePlan", ObjectType(
            Property("id", StringType),
            Property("code", StringType),
            Property("name", StringType),
            Property("description", StringType),
            Property("isSubjectToCityTax", BooleanType),
        )),
        Property("unitGroup", ObjectType(
            Property("id", StringType),
            Property("code", StringType),
            Property("name", StringType),
            Property("description", StringType),
            Property("type", StringType),
        )),
        Property("unit", ObjectType(
            Property("id", StringType),
            Property("name", StringType),
            Property("description", StringType),
            Property("unitGroupId", StringType),
        )),
        Property("totalGrossAmount", ObjectType(
            Property("amount", NumberType),
            Property("currency", StringType),
        )),
        Property("arrival", DateTimeType),
        Property("departure", DateTimeType),
        Property("created", DateTimeType),
        Property("modified", DateTimeType),
        Property("adults", IntegerType),
        
    ).to_dict()

"""         Property("", StringType),
        Property("", StringType),
        Property("", StringType),
        Property("", StringType),
        Property("", StringType),
        Property("", StringType),
        Property("", StringType),
        Property("", ObjectType(
            Property("", StringType),
            Property("", StringType),
            Property("", StringType),
            Property("", StringType),
            Property("", StringType),
            Property("", StringType),
            Property("", StringType),
            Property("", StringType),
            Property("", StringType),
        )), """
