import aiosqlite

DB_NAME = "database.db"


async def connect():
    return await aiosqlite.connect(DB_NAME)


async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute("""
        CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            full_name TEXT,
            balance REAL DEFAULT 0,
            referred_by INTEGER,
            referrals INTEGER DEFAULT 0,
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS products(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS stock(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            account TEXT,
            sold INTEGER DEFAULT 0
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS deposits(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            method TEXT,
            usd REAL,
            bdt REAL,
            txid TEXT UNIQUE,
            status TEXT DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS purchases(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            product_id INTEGER,
            account TEXT,
            price REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS reviews(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            review TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        await db.commit()


# ================= USERS =================

async def add_user(user_id, username, full_name):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            INSERT OR IGNORE INTO users(user_id, username, full_name)
            VALUES(?,?,?)
            """,
            (user_id, username, full_name)
        )
        await db.commit()


async def get_user(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT * FROM users WHERE user_id=?",
            (user_id,)
        )
        return await cursor.fetchone()


async def get_balance(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT balance FROM users WHERE user_id=?",
            (user_id,)
        )
        row = await cursor.fetchone()
        return row[0] if row else 0


async def update_balance(user_id, amount):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            UPDATE users
            SET balance = balance + ?
            WHERE user_id=?
            """,
            (amount, user_id)
        )
        await db.commit()


# ================= REFERRAL =================

async def has_referrer(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            """
            SELECT referred_by
            FROM users
            WHERE user_id=?
            """,
            (user_id,)
        )
        row = await cursor.fetchone()

        if row and row[0]:
            return True
        return False


async def set_referrer(user_id, referrer_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            UPDATE users
            SET referred_by=?
            WHERE user_id=?
            """,
            (referrer_id, user_id)
        )

        await db.execute(
            """
            UPDATE users
            SET referrals = referrals + 1
            WHERE user_id=?
            """,
            (referrer_id,)
        )

        await db.commit()


async def get_referrals(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            """
            SELECT referrals
            FROM users
            WHERE user_id=?
            """,
            (user_id,)
        )
        row = await cursor.fetchone()
        return row[0] if row else 0

# ================= PRODUCTS =================

async def get_products():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("""
            SELECT id, name, price
            FROM products
            ORDER BY id ASC
        """)
        return await cursor.fetchall()


async def get_product(product_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("""
            SELECT id, name, price, description
            FROM products
            WHERE id=?
        """, (product_id,))
        return await cursor.fetchone()


async def add_product(name, price, description):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("""
            INSERT INTO products(name, price, description)
            VALUES(?,?,?)
        """, (name, price, description))
        await db.commit()
        return cursor.lastrowid


# ================= STOCK =================

async def add_stock(product_id, account):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            INSERT INTO stock(product_id, account)
            VALUES(?,?)
        """, (product_id, account))
        await db.commit()


async def get_stock_count(product_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("""
            SELECT COUNT(*)
            FROM stock
            WHERE product_id=? AND sold=0
        """, (product_id,))
        row = await cursor.fetchone()
        return row[0]


async def get_available_stock(product_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("""
            SELECT id, account
            FROM stock
            WHERE product_id=? AND sold=0
            LIMIT 1
        """, (product_id,))
        return await cursor.fetchone()


async def mark_stock_sold(stock_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "UPDATE stock SET sold=1 WHERE id=?",
            (stock_id,)
        )
        await db.commit()


# ================= PURCHASE =================

async def add_purchase(user_id, product_id, account, price):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            INSERT INTO purchases(
                user_id,
                product_id,
                account,
                price
            )
            VALUES(?,?,?,?)
        """, (
            user_id,
            product_id,
            account,
            price
        ))
        await db.commit()


# ================= DEPOSIT =================

async def txid_exists(txid):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT id FROM deposits WHERE txid=?",
            (txid,)
        )
        return await cursor.fetchone()


async def add_deposit(user_id, method, usd, bdt, txid):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            INSERT INTO deposits(
                user_id,
                method,
                usd,
                bdt,
                txid
            )
            VALUES(?,?,?,?,?)
        """, (
            user_id,
            method,
            usd,
            bdt,
            txid
        ))
        await db.commit()


async def get_user_deposits(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("""
            SELECT method, usd, status, created_at
            FROM deposits
            WHERE user_id=?
            ORDER BY id DESC
        """, (user_id,))
        return await cursor.fetchall()


# ================= REVIEWS =================

async def add_review(user_id, review):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            INSERT INTO reviews(user_id, review)
            VALUES(?,?)
        """, (
            user_id,
            review
        ))
        await db.commit()


async def get_reviews(limit=10):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("""
            SELECT review
            FROM reviews
            ORDER BY id DESC
            LIMIT ?
        """, (limit,))
        return await cursor.fetchall()


# ================= STATS =================

async def total_users():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT COUNT(*) FROM users")
        return (await cursor.fetchone())[0]


async def total_products():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT COUNT(*) FROM products")
        return (await cursor.fetchone())[0]


async def total_deposits():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT COUNT(*) FROM deposits")
        return (await cursor.fetchone())[0]


async def total_purchases():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT COUNT(*) FROM purchases")
        return (await cursor.fetchone())[0]


async def reward_referrer(referrer_id, amount):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            UPDATE users
            SET balance = balance + ?
            WHERE user_id=?
            """,
            (amount, referrer_id)
        )
        await db.commit()
