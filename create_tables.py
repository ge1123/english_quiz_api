# create_tables.py
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from models.user import Base
from urllib.parse import quote_plus

dsn = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=172.28.167.25,1761;"
    "Database=EnglishQuiz;"
    "UID=sa;"
    "PWD=P@55word;"
)
encoded_dsn = quote_plus(dsn)
DATABASE_URL = f"mssql+aioodbc:///?odbc_connect={encoded_dsn}"

engine = create_async_engine(DATABASE_URL, echo=True)


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(init_models())
