import re
from api.conf.config import settings


class CrossOriginRequestSharing:
    """
    Creates a new CORS config object.

        :param origins: list of origins to add as a CORS HTTP header value
        :type origins: list[str] | None
        :param allow_credentials: whether allow credentials in CORS or not
        :type allow_credentials: bool
        :param allow_methods: list of allowed methods
        :type allow_methods: list[str] | None
        :param allow_headers: list of allowed headers
        :type allow_headers: list[str] | None
    """
    WILDCARD_ALL_ALLOWED = ['*']

    def __init__(self, origins: list[str] = None, allow_credentials=True,
                 allow_methods: list[str] = None, allow_headers: list[str] = None):
        self.origins = origins
        self.allow_credentials = allow_credentials
        self.allow_methods = allow_methods or CrossOriginRequestSharing.WILDCARD_ALL_ALLOWED
        self.allow_headers = allow_headers or CrossOriginRequestSharing.WILDCARD_ALL_ALLOWED


CORS = CrossOriginRequestSharing(
    origins=re.split(r'\s*,\s*', settings.cors_origins)
)
