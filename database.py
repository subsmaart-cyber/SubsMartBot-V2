import aiosqlite
from config import DATABASE_NAME


async def init_db():
    async with aiosqlite.connect(DATABASE_NAME) as db:

        await db.execute("""
        CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            full_name TEXT,
            balance REAL DEFAULT 0,
            referral_balance REAL DEFAULT 0,
            referred_by INTEGER,
            referral_count INTEGER DEFAULT 0,
            joined INTEGER DEFAULT 0,
            banned INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        await db.commit()
