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
            return rows  # Return the result

# Asynchronous function to fetch users older than 40


async def async_fetch_older_users():
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            rows = await cursor.fetchall()
            print("\nUsers Older Than 40:")
            for row in rows:
                print(row)
            return rows  # Return the result

# Run both queries concurrently


async def fetch_concurrently():
    all_users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    # Results are returned and can be further processed here if needed
    print("\nResults Retrieved for Further Processing:")
    print("All Users:", all_users)
    print("Users Older Than 40:", older_users)

# Main entry point
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
