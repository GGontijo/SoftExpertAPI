class SoftExpertOptions:

    def __init__(self, url: str, authorization: str, userID: str):
        """
        Initialize the SoftExpertOptions with the given url and token.

        :param url: The base URL of the API.
        :param token: The authentication token.
        """
        self.url = url
        self.authorization = authorization
        self.userID = userID

