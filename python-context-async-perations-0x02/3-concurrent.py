import asyncio
import aiosqlite

DATABASE = "alx-prodev.db"

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

# Run both queries concurrently and add checks


async def fetch_concurrently():
    all_users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

    # Check 1: Validate that the results are lists
    assert isinstance(
        all_users, list), "async_fetch_users() must return a list"
    assert isinstance(
        older_users, list), "async_fetch_older_users() must return a list"

    # Check 2: Ensure users older than 40 are correctly filtered
    for user in older_users:
        assert user[1] > 40, f"User {user} does not meet the age > 40 condition"

    # Check 3: Ensure the total number of users is greater than or equal to the number of older users
    assert len(all_users) >= len(older_users), (
        "The total number of users should be greater than or equal to users older than 40"
    )

    print("\nValidation Passed!")
    return all_users, older_users

# Main entry point
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
