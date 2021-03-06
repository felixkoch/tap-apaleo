"""REST client handling, including ApaleoStream base class."""

import requests
from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from memoization import cached

from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.streams import RESTStream

from tap_apaleo.auth import ApaleoAuthenticator


SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class ApaleoStream(RESTStream):
    """Apaleo stream class."""

    url_base = "https://api.apaleo.com"

    # OR use a dynamic url_base:
    # @property
    # def url_base(self) -> str:
    #     """Return the API URL root, configurable via tap settings."""
    #     return self.config["api_url"]

    #records_jsonpath = "$[*]"  # Or override `parse_response`.
    #next_page_token_jsonpath = "$.next_page"  # Or override `get_next_page_token`.

    @property
    @cached
    def authenticator(self) -> ApaleoAuthenticator:
        """Return a new authenticator object."""
        return ApaleoAuthenticator.create_for_stream(self)

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed."""
        headers = {}
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")
        return headers

    def get_next_page_token(
        self, response: requests.Response, previous_token: Optional[Any]
    ) -> Optional[Any]:
        """Return a token for identifying next page or None if no more pages."""

        if(response.status_code == 204):
            return None

        previous_token = previous_token or 1
        data = response.json()
        size = 1000
        count = data["count"]

        if previous_token*size >= count:
            return None

        return previous_token + 1

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        params: dict = {}
        params["pageSize"] = 1000
        if next_page_token:
            params["pageNumber"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key
        self.logger.info(params)    
        return params

    def prepare_request_payload(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Optional[dict]:
        """Prepare the data payload for the REST API request.

        By default, no payload will be sent (return None).
        """
        # TODO: Delete this method if no payload is required. (Most REST APIs.)
        return None

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result rows."""
        # TODO: Parse response body and return a set of records.
        if(response.status_code == 204):
            return None
        
        yield from extract_jsonpath(self.records_jsonpath, input=response.json())

    #def post_process(self, row: dict, context: Optional[dict]) -> dict:
    #    """As needed, append or transform raw data to match expected structure."""
    #    # Delete this method if not needed.
    #    return row
