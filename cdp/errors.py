import json
from decimal import Decimal

from cdp.client.exceptions import ApiException


class APIError(Exception):
    def __init__(
        self,
        err: ApiException,
        code: str | None = None,
        message: str | None = None,
        unhandled: bool = False,
    ) -> None:
        self._http_code = err.status
        self._api_code = code
        self._api_message = message
        self._handled = bool(code and message and not unhandled)
        super().__init__(str(err))

    @classmethod
    def from_error(cls, err: ApiException) -> "APIError":
        if not isinstance(err, ApiException):
            raise ValueError("argument must be an ApiException")

        if not err.body:
            return cls(err)

        try:
            body = json.loads(err.body)
        except json.JSONDecodeError:
            return cls(err)

        message = body.get("message")
        code = body.get("code")

        if code in ERROR_CODE_TO_ERROR_CLASS:
            return ERROR_CODE_TO_ERROR_CLASS[code](err, code=code, message=message)
        else:
            return cls(err, code=code, message=message, unhandled=True)

    @property
    def http_code(self) -> int:
        return self._http_code

    @property
    def api_code(self) -> str | None:
        return self._api_code

    @property
    def api_message(self) -> str | None:
        return self._api_message

    @property
    def handled(self) -> bool:
        return self._handled

    def __str__(self) -> str:
        if self.handled:
            return f"APIError(http_code={self.http_code}, api_code={self.api_code}, api_message={self.api_message})"
        else:
            return f"APIError(http_code={self.http_code}, api_code={self.api_code}, api_message={self.api_message}, unhandled=True)"


class InvalidConfigurationError(Exception):
    """Exception raised for errors in the configuration of the Coinbase SDK."""

    def __init__(self, message: str = "Invalid configuration provided") -> None:
        self.message = message
        super().__init__(self.message)


class InvalidAPIKeyFormatError(Exception):
    """Exception raised for errors in the format of the API key."""

    def __init__(self, message: str = "Invalid API key format") -> None:
        self.message = message
        super().__init__(self.message)


class InsufficientFundsError(Exception):
    """An error raised when an operation is attempted with insufficient funds."""

    def __init__(self, expected: Decimal, exact: Decimal, msg: str = "Insufficient funds") -> None:
        """Initialize the InsufficientFundsError.

        Args:
            expected (Decimal): The expected amount of funds.
            exact (Decimal): The actual amount of funds available.
            msg (str): The error message prefix.

        """
        super().__init__(f"{msg}: have {exact}, need {expected}.")


class AlreadySignedError(Exception):
    """An error raised when a resource is already signed."""

    def __init__(self, msg: str = "Resource already signed") -> None:
        """Initialize the AlreadySignedError.

        Args:
            msg (str): The error message.

        """
        super().__init__(msg)


class TransactionNotSignedError(Exception):
    """An error raised when a transaction is not signed."""

    def __init__(self, msg: str = "Transaction must be signed") -> None:
        """Initialize the TransactionNotSignedError.

        Args:
            msg (str): The error message.

        """
        super().__init__(msg)


class AddressCannotSignError(Exception):
    """An error raised when an address attempts to sign a transaction without a private key."""

    def __init__(
        self, msg: str = "Address cannot sign transaction without private key loaded"
    ) -> None:
        """Initialize the AddressCannotSignError.

        Args:
            msg (str): The error message.

        """
        super().__init__(msg)


class UnimplementedError(APIError):
    """Exception raised for unimplemented features in the Coinbase SDK."""

    pass


class UnauthorizedError(APIError):
    """Exception raised for unauthorized access to Coinbase API endpoints."""

    pass


class InternalError(APIError):
    """Exception raised for internal server errors."""

    pass


class NotFoundError(APIError):
    """Exception raised when a requested resource is not found."""

    pass


class InvalidWalletIDError(APIError):
    """Exception raised for invalid wallet ID."""

    pass


class InvalidAddressIDError(APIError):
    """Exception raised for invalid address ID."""

    pass


class InvalidWalletError(APIError):
    """Exception raised for invalid wallet."""

    pass


class InvalidAddressError(APIError):
    """Exception raised for invalid address."""

    pass


class InvalidAmountError(APIError):
    """Exception raised for invalid amount."""

    pass


class InvalidTransferIDError(APIError):
    """Exception raised for invalid transfer ID."""

    pass


class InvalidPageError(APIError):
    """Exception raised for invalid page token."""

    pass


class InvalidLimitError(APIError):
    """Exception raised for invalid page limit."""

    pass


class AlreadyExistsError(APIError):
    """Exception raised when a resource already exists."""

    pass


class MalformedRequestError(APIError):
    """Exception raised for malformed requests."""

    pass


class UnsupportedAssetError(APIError):
    """Exception raised for unsupported assets."""

    pass


class InvalidAssetIDError(APIError):
    """Exception raised for invalid asset ID."""

    pass


class InvalidDestinationError(APIError):
    """Exception raised for invalid destination."""

    pass


class InvalidNetworkIDError(APIError):
    """Exception raised for invalid network ID."""

    pass


class ResourceExhaustedError(APIError):
    """Exception raised when a resource is exhausted."""

    pass


class FaucetLimitReachedError(APIError):
    """Exception raised when the faucet limit is reached."""

    pass


class InvalidSignedPayloadError(APIError):
    """Exception raised for invalid signed payload."""

    pass


class InvalidTransferStatusError(APIError):
    """Exception raised for invalid transfer status."""

    pass


class NetworkFeatureUnsupportedError(APIError):
    """Exception raised when a network feature is unsupported."""

    pass


ERROR_CODE_TO_ERROR_CLASS: dict[str, type[APIError]] = {
    "unimplemented": UnimplementedError,
    "unauthorized": UnauthorizedError,
    "internal": InternalError,
    "not_found": NotFoundError,
    "invalid_wallet_id": InvalidWalletIDError,
    "invalid_address_id": InvalidAddressIDError,
    "invalid_wallet": InvalidWalletError,
    "invalid_address": InvalidAddressError,
    "invalid_amount": InvalidAmountError,
    "invalid_transfer_id": InvalidTransferIDError,
    "invalid_page_token": InvalidPageError,
    "invalid_page_limit": InvalidLimitError,
    "already_exists": AlreadyExistsError,
    "malformed_request": MalformedRequestError,
    "unsupported_asset": UnsupportedAssetError,
    "invalid_asset_id": InvalidAssetIDError,
    "invalid_destination": InvalidDestinationError,
    "invalid_network_id": InvalidNetworkIDError,
    "resource_exhausted": ResourceExhaustedError,
    "faucet_limit_reached": FaucetLimitReachedError,
    "invalid_signed_payload": InvalidSignedPayloadError,
    "invalid_transfer_status": InvalidTransferStatusError,
    "network_feature_unsupported": NetworkFeatureUnsupportedError,
}