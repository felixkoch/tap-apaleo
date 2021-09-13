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
        Property("created", DateTimeType),
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
        starting_timestamp = self.get_starting_timestamp(context)
        self.logger.info(starting_timestamp)

        self.logger.info(next_page_token)
        params: dict = {}
        params["pageSize"] = 1000
        if next_page_token:
            params["pageNumber"] = next_page_token

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
            Property("name", StringType),
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
        Property("childrenAges", ArrayType(IntegerType)),
        Property("comment", StringType),
        Property("guestComment", StringType),
        Property("externalCode", StringType),
        Property("channelCode", StringType),
        Property("source", StringType),
        Property("primaryGuest", ObjectType(
            Property("title", StringType),
            Property("gender", StringType),
            Property("firstName", StringType),
            Property("middleInitial", StringType),
            Property("lastName", StringType),
            Property("email", StringType),
            Property("phone", StringType),
            Property("address", ObjectType(
                Property("addressLine1", StringType),
                Property("addressLine2", StringType),
                Property("postalCode", StringType),
                Property("city", StringType),
                Property("regionCode", StringType),
                Property("countryCode", StringType),

            )),
            Property("nationalityCountryCode", StringType),
            Property("identificationNumber", StringType),
            Property("identificationIssueDate", DateTimeType),
            Property("identificationType", StringType),
            Property("company", ObjectType(
                Property("name", StringType),
                Property("taxId", StringType),
            )),
            Property("preferredLanguage", StringType),
            Property("birthDate", DateTimeType),
            Property("birthPlace", StringType),
        )),
        Property("additionalGuests", ArrayType(ObjectType(
            Property("title", StringType),
            Property("gender", StringType),
            Property("firstName", StringType),
            Property("middleInitial", StringType),
            Property("lastName", StringType),
            Property("email", StringType),
            Property("phone", StringType),
            Property("address", ObjectType(
                Property("addressLine1", StringType),
                Property("addressLine2", StringType),
                Property("postalCode", StringType),
                Property("city", StringType),
                Property("regionCode", StringType),
                Property("countryCode", StringType),

            )),
            Property("nationalityCountryCode", StringType),
            Property("identificationNumber", StringType),
            Property("identificationIssueDate", DateTimeType),
            Property("identificationType", StringType),
            Property("company", ObjectType(
                Property("name", StringType),
                Property("taxId", StringType),
            )),
            Property("preferredLanguage", StringType),
            Property("birthDate", DateTimeType),
            Property("birthPlace", StringType),
        ))),
        Property("booker", ObjectType(
            Property("title", StringType),
            Property("gender", StringType),
            Property("firstName", StringType),
            Property("middleInitial", StringType),
            Property("lastName", StringType),
            Property("email", StringType),
            Property("phone", StringType),
            Property("address", ObjectType(
                Property("addressLine1", StringType),
                Property("addressLine2", StringType),
                Property("postalCode", StringType),
                Property("city", StringType),
                Property("regionCode", StringType),
                Property("countryCode", StringType),

            )),
            Property("nationalityCountryCode", StringType),
            Property("identificationNumber", StringType),
            Property("identificationIssueDate", DateTimeType),
            Property("identificationType", StringType),
            Property("company", ObjectType(
                Property("name", StringType),
                Property("taxId", StringType),
            )),
            Property("preferredLanguage", StringType),
            Property("birthDate", DateTimeType),
            Property("birthPlace", StringType),
        )),
        Property("paymentAccount", ObjectType(
            Property("accountNumber", StringType),
            Property("accountHolder", StringType),
            Property("expiryMonth", StringType),
            Property("expiryYear", StringType),
            Property("paymentMethod", StringType),
            Property("payerEmail", StringType),
            Property("payerReference", StringType),
            Property("isVirtual", BooleanType),
            Property("isActive", BooleanType),
            Property("inactiveReason", StringType),
        )),
        Property("guaranteeType", StringType),
        Property("cancellationFee", ObjectType(
            Property("id", StringType),
            Property("code", StringType),
            Property("name", StringType),
            Property("description", StringType),
            Property("dueDateTime", DateTimeType),
            Property("fee", ObjectType(
                Property("amount", NumberType),
                Property("currency", StringType),
            )),
        )),
        Property("noShowFee", ObjectType(
            Property("id", StringType),
            Property("code", StringType),
            Property("name", StringType),
            Property("description", StringType),
            Property("fee", ObjectType(
                Property("amount", NumberType),
                Property("currency", StringType),
            )),
        )),
        Property("travelPurpose", StringType),
        Property("balance", ObjectType(
            Property("amount", NumberType),
            Property("currency", StringType),
        )),
        Property("assignedUnits", ArrayType(ObjectType(
            Property("unit", ObjectType(
                Property("id", StringType),
                Property("name", StringType),
                Property("description", StringType),
                Property("unitGroupId", StringType),
            )),
            Property("timeRanges", ArrayType(ObjectType(
                Property("from", DateTimeType),
                Property("to", DateTimeType),
            )))
        ))),
        Property("timeSlices", ArrayType(ObjectType(
            Property("from", DateTimeType),
            Property("to", DateTimeType),
            Property("serviceDate", DateTimeType),
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
            Property("baseAmount", ObjectType(
                Property("grossAmount", NumberType),
                Property("netAmount", NumberType),
                Property("vatType", StringType),
                Property("vatPercent", NumberType),
                Property("currency", StringType),
            )),
            Property("totalGrossAmount", ObjectType(
                Property("amount", NumberType),
                Property("currency", StringType),
            )),
            Property("includedServices", ArrayType(ObjectType(
                Property("service", ObjectType(
                    Property("id", StringType),
                    Property("code", StringType),
                    Property("name", StringType),
                    Property("description", StringType),
                )),
                Property("serviceDate", DateTimeType),
                Property("count", IntegerType),
                Property("amount", ObjectType(
                    Property("grossAmount", NumberType),
                    Property("netAmount", NumberType),
                    Property("vatType", StringType),
                    Property("vatPercent", NumberType),
                    Property("currency", StringType),
                )),
                Property("bookedAsExtra", BooleanType),

            ))),
            Property("actions", ArrayType(ObjectType(
                Property("action", StringType),
                Property("isAllowed", BooleanType),
                Property("reasons", ArrayType(ObjectType(
                    Property("code", StringType),
                    Property("message", StringType),
                ))),
            )))
        ))),
        Property("services", ArrayType(ObjectType(
            Property("service", ObjectType(
                Property("id", StringType),
                Property("code", StringType),
                Property("name", StringType),
                Property("description", StringType),
                Property("pricingUnit", StringType),
                Property("defaultGrossPrice", ObjectType(
                    Property("amount", NumberType),
                    Property("currency", StringType),
                )),
            )),
            Property("totalAmount", ObjectType(
                Property("grossAmount", NumberType),
                Property("netAmount", NumberType),
                Property("vatType", StringType),
                Property("vatPercent", NumberType),
                Property("currency", StringType),
            )),
            Property("dates", ArrayType(ObjectType(
                Property("serviceDate", DateTimeType),
                Property("count", IntegerType),
                Property("amount", ObjectType(
                    Property("grossAmount", NumberType),
                    Property("netAmount", NumberType),
                    Property("vatType", StringType),
                    Property("vatPercent", NumberType),
                    Property("currency", StringType),
                )),
                Property("isMandatory", BooleanType)
            )))
        ))),
        Property("validationMessages", ArrayType(ObjectType(
            Property("category", StringType),
            Property("code", StringType),
            Property("message", StringType),
        ))),
        Property("actions", ArrayType(ObjectType(
            Property("action", StringType),
            Property("isAllowed", BooleanType),
            Property("reasons", ArrayType(ObjectType(
                Property("code", StringType),
                Property("message", StringType),
            ))),
        ))),
        Property("company", ObjectType(
            Property("id", StringType),
            Property("code", StringType),
            Property("name", StringType),
            Property("canCheckOutOnAr", BooleanType),
        )),
        Property("corporateCode", StringType),
        Property("allFoliosHaveInvoice", BooleanType),
        Property("hasCityTax", BooleanType),
        Property("commission", ObjectType(
            Property("commissionAmount", ObjectType(
                Property("amount", NumberType),
                Property("currency", StringType),
            )),
            Property("beforeCommissionAmount", ObjectType(
                Property("amount", NumberType),
                Property("currency", StringType),
            )),
        )),
        Property("promoCode", StringType),
    ).to_dict()


class UnitGroupsStream(ApaleoStream):
    """Define custom stream."""
    name = "unit-groups"
    path = "/inventory/v1/unit-groups"
    primary_keys = ["id"]
    replication_key = None
    records_jsonpath = "$.unitGroups[*]"

    schema = PropertiesList(
        Property("id", StringType),
        Property("code", StringType),
        Property("name", StringType),
        Property("description", StringType),
        Property("memberCount", IntegerType),
        Property("maxPersons", IntegerType),
        Property("rank", IntegerType),
        Property("type", StringType),
        Property("property", ObjectType(
            Property("id", StringType),
            Property("code", StringType),
            Property("name", StringType),
            Property("description", StringType),
        )),
    ).to_dict()


class UnitsStream(ApaleoStream):
    """Define custom stream."""
    name = "units"
    path = "/inventory/v1/units"
    primary_keys = ["id"]
    replication_key = None
    records_jsonpath = "$.units[*]"

    schema = PropertiesList(
        Property("id", StringType),
        Property("name", StringType),
        Property("description", StringType),
        Property("property", ObjectType(
            Property("id", StringType),
            Property("code", StringType),
            Property("name", StringType),
            Property("description", StringType),
        )),
        Property("unitGroup", ObjectType(
            Property("id", StringType),
            Property("code", StringType),
            Property("name", StringType),
            Property("description", StringType),
            Property("type", StringType),
        )),
        Property("status", ObjectType(
            Property("isOccupied", BooleanType),
            Property("condition", StringType),
            Property("maintenance", ObjectType(
                Property("id", StringType),
                Property("type", StringType),
            )),
        )),
        Property("maxPersons", IntegerType),
        Property("created", DateTimeType),
        Property("attributes", ArrayType(ObjectType(
            Property("id", StringType),
            Property("name", StringType),
            Property("description", StringType),
        )))

    ).to_dict()


class RatePlansStream(ApaleoStream):
    """Define custom stream."""
    name = "rate-plans"
    path = "/rateplan/v1/rate-plans"
    primary_keys = ["id"]
    replication_key = None
    records_jsonpath = "$.ratePlans[*]"

    schema = PropertiesList(
        Property("id", StringType),
        Property("code", StringType),
        Property("name", StringType),
        Property("description", StringType),
        Property("minGuaranteeType", StringType),
        Property("priceCalculationMode", StringType),
        Property("property", ObjectType(
            Property("id", StringType),
            Property("code", StringType),
            Property("name", StringType),
            Property("description", StringType),
        )),
        Property("unitGroup", ObjectType(
            Property("id", StringType),
            Property("code", StringType),
            Property("name", StringType),
            Property("description", StringType),
            Property("type", StringType),
        )),
        Property("cancellationPolicy", ObjectType(
            Property("id", StringType),
            Property("code", StringType),
            Property("name", StringType),
            Property("description", StringType),
            Property("periodPriorToArrival", ObjectType(
                Property("hours", IntegerType),
                Property("days", IntegerType),
                Property("months", IntegerType),
            )),
        )),
        Property("noShowPolicy", ObjectType(
            Property("id", StringType),
            Property("code", StringType),
            Property("name", StringType),
            Property("description", StringType),
        )),
        Property("channelCodes", ArrayType(StringType)),
        Property("promoCodes", ArrayType(StringType)),
        Property("timeSliceDefinition", ObjectType(
            Property("id", StringType),
            Property("name", StringType),
            Property("template", StringType),
            Property("checkInTime", StringType),
            Property("checkOutTime", StringType),
        )),
        Property("restrictions", ObjectType(
            Property("minAdvance", ObjectType(
                Property("hours", IntegerType),
                Property("days", IntegerType),
                Property("months", IntegerType),
            )),
            Property("maxAdvance", ObjectType(
                Property("hours", IntegerType),
                Property("days", IntegerType),
                Property("months", IntegerType),
            )),
            Property("lateBookingUntil", StringType),
        )),
        Property("bookingPeriods", ArrayType(ObjectType(
            Property("from", DateTimeType),
            Property("to", DateTimeType),
        ))),
        Property("isBookable", BooleanType),
        Property("isSubjectToCityTax", BooleanType),
        Property("pricingRule", ObjectType(
            Property("baseRatePlan", ObjectType(
                Property("id", StringType),
                Property("code", StringType),
                Property("name", StringType),
                Property("description", StringType),
                Property("isSubjectToCityTax", BooleanType),
            )),
            Property("type", StringType),
            Property("value", NumberType),
        )),
        Property("isDerived", BooleanType),
        Property("derivationLevel", IntegerType),
        Property("surcharges", ArrayType(ObjectType(
            Property("adults", IntegerType),
            Property("type", StringType),
            Property("value", NumberType),
        ))),
        Property("ageCategories", ArrayType(ObjectType(
            Property("id", StringType),
            Property("surcharges", ArrayType(ObjectType(
                Property("adults", IntegerType),
                Property("value", NumberType),
            ))),
        ))),
        Property("includedServices", ArrayType(ObjectType(
            Property("service", ObjectType(
                Property("id", StringType),
                Property("code", StringType),
                Property("name", StringType),
                Property("description", StringType),
            )),
            Property("grossPrice", ObjectType(
                Property("amount", NumberType),
                Property("currency", StringType),
            )),
            Property("pricingMode", StringType),

        ))),
        Property("companies", ArrayType(ObjectType(
            Property("id", StringType),
            Property("code", StringType),
            Property("corporateCode", StringType),
            Property("name", StringType),
        ))),
        Property("ratesRange", ObjectType(
            Property("from", DateTimeType),
            Property("to", DateTimeType),
        )),
        Property("accountingConfigs", ArrayType(ObjectType(
            Property("vatType", StringType),
            Property("serviceType", StringType),
            Property("subAccountId", StringType),
            Property("validFrom", DateTimeType),
        ))),

    ).to_dict()


class MaintenancesStream(ApaleoStream):
    """Define custom stream."""
    name = "maintenances"
    path = "/operations/v1/maintenances"
    primary_keys = ["id"]
    replication_key = None
    records_jsonpath = "$.maintenances[*]"

    schema = PropertiesList(
        Property("id", StringType),
        Property("unit", ObjectType(
            Property("id", StringType),
            Property("name", StringType),
            Property("description", StringType),
            Property("unitGroupId", StringType),

        )),
        Property("from", DateTimeType),
        Property("to", DateTimeType),
        Property("type", StringType),
        Property("description", StringType),

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
