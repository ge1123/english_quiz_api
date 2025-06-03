import asyncio
import aioodbc


async def test_connection():
    dsn = (
        "Driver={ODBC Driver 17 for SQL Server};"
        "Server=172.28.167.25,1761;"
        "Database=EnglishQuiz;"
        "UID=sa;"
        "PWD=P@55word;"
    )
    conn = await aioodbc.connect(dsn=dsn)
    cursor = await conn.cursor()
    await cursor.execute("SELECT top 1 * from WordList ")
    result = await cursor.fetchone()
    print(result)
    await cursor.close()
    await conn.close()


asyncio.run(test_connection())
