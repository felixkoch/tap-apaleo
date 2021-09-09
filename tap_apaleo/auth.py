"""Apaleo Authentication."""


from singer_sdk.authenticators import OAuthAuthenticator, SingletonMeta


# The SingletonMeta metaclass makes your streams reuse the same authenticator instance.
# If this behaviour interferes with your use-case, you can remove the metaclass.
class ApaleoAuthenticator(OAuthAuthenticator, metaclass=SingletonMeta):
    """Authenticator class for Apaleo."""

    @property
    def oauth_request_body(self) -> dict:
        """Define the OAuth request body for the Apaleo API."""
        # Define the request body needed for the API.
        return {
            #'resource': 'https://api.apaleo.com/',
            #'scope': self.oauth_scopes,
            'client_id': self.config["client_id"],
            'client_secret': self.config["client_secret"],
            'grant_type': 'client_credentials',
        }

    @classmethod
    def create_for_stream(cls, stream) -> "ApaleoAuthenticator":
        return cls(
            stream=stream,
            auth_endpoint="https://identity.apaleo.com/connect/token",
            #oauth_scopes="OAuth Scopes",
        )
