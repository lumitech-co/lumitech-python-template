class DatabaseInitializationError(Exception):
    def __init__(self) -> None:
        super().__init__("Database is not initialized.")
