import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus

# 建立 DSN 字串（注意要做 URI 編碼）
dsn = (
    "Driver={ODBC Driver 17 for SQL Server};"
    f"Server={os.getenv('DB_SERVER', '172.28.167.25,1761')};"
    f"Database={os.getenv('DB_NAME', 'EnglishQuiz')};"
    f"UID={os.getenv('DB_USER', 'sa')};"
    f"PWD={os.getenv('DB_PASSWORD', 'P@55word')};"
)

# URI encode dsn
encoded_dsn = quote_plus(dsn)

# 用 aioodbc 建立 sqlalchemy 的 async engine
DATABASE_URL = f"mssql+aioodbc:///?odbc_connect={encoded_dsn}"

# 建立 SQLAlchemy async engine & session
engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


# 提供 FastAPI 使用的依賴
async def get_async_session():
    async with AsyncSessionLocal() as session:
        yield session
