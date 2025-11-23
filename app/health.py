import os
import asyncpg
from app.logger import logger


DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@postgres:5432/postgres")


async def check_db():
"""Return (ok: bool, details: dict). Attempts a short DB connection and simple query."""
try:
conn = await asyncpg.connect(DATABASE_URL)
# quick ping
await conn.execute("SELECT 1")
await conn.close()
return True, {"db": "connected"}
except Exception as e:
logger.exception("db_health_check_failed", extra={"error": str(e)})
return False, {"db": "disconnected", "error": str(e)}
