class BaseballAPIException(Exception):
    def __init__(self, message: str = "Error fetching data from Baseball API"):
        super().__init__(message)
