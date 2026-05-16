class DataNotFoundError(Exception):
    """
    Raised when a valid request produces no matching analytics data.

    This maps to HTTP 404 in the FastAPI exception handler.
    """

    def __init__(self, message: str = "No data found for the requested filters.") -> None:
        self.message = message
        super().__init__(message)