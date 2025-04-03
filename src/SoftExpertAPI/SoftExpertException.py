class SoftExpertException(Exception):
    """Classe de exceções personalizadas para erros no SoftExpert."""

    def __init__(self, message, data: any = None):
        self.message = message
        super().__init__(message)
        self.data = data
