import asyncio
import aiosqlite

DATABASE = "example.db"

# Asynchronous function to fetch all users


async def async_fetch_users():
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            rows = await cursor.fetchall()
            print("All Users:")
            for row in rows:
                print(row)

# Asynchronous function to fetch users older than 40


async def async_fetch_older_users():
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            rows = await cursor.fetchall()
            print("\nUsers Older Than 40:")
            for row in rows:
                print(row)

# Run both queries concurrently


async def fetch_concurrently():
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

# Main entry point
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
