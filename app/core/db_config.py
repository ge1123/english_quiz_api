from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_server: str
    db_name: str
    db_user: str
    db_password: str

    @property
    def database_url(self) -> str:
        from urllib.parse import quote_plus
        dsn = (
            f"Driver={{ODBC Driver 17 for SQL Server}};"
            f"Server={self.db_server};"
            f"Database={self.db_name};"
            f"UID={self.db_user};"
            f"PWD={self.db_password};"
        )
        return f"mssql+aioodbc:///?odbc_connect={quote_plus(dsn)}"

    class Config:
        env_file = ".env"

settings = Settings()
