class PropertyTestingException(Exception):
    def __init__(self, message: str) -> None:
        self.message: str = message
        super().__init__(self.message)
