"""
Database usage example
"""

from src.core.database import Database
from src.utils.logger import get_logger


def main():
    """Demonstrate database operations"""

    logger = get_logger(level='INFO')
    logger.info("Database example started")

    # Create database
    db = Database(':memory:')
    db.connect()

    # Create table
    db.create_table('users', {
        'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'name': 'TEXT NOT NULL',
        'email': 'TEXT UNIQUE',
        'age': 'INTEGER'
    })

    # Insert data
    user_id = db.insert('users', {
        'name': 'John Doe',
        'email': 'john@example.com',
        'age': 30
    })
    logger.info(f"Inserted user with ID: {user_id}")

    # Insert more users
    db.insert('users', {'name': 'Jane Smith', 'email': 'jane@example.com', 'age': 25})
    db.insert('users', {'name': 'Bob Johnson', 'email': 'bob@example.com', 'age': 35})

    # Query all users
    users = db.fetch_all('SELECT * FROM users')
    logger.info(f"All users: {users}")

    # Query specific user
    user = db.fetch_one('SELECT * FROM users WHERE email = ?', ('john@example.com',))
    logger.info(f"Found user: {user}")

    # Update user
    rows_updated = db.update(
        'users',
        {'age': 31},
        'email = ?',
        ('john@example.com',)
    )
    logger.info(f"Updated {rows_updated} rows")

    # Delete user
    rows_deleted = db.delete('users', 'age > ?', (30,))
    logger.info(f"Deleted {rows_deleted} rows")

    # Final count
    remaining = db.fetch_all('SELECT * FROM users')
    logger.info(f"Remaining users: {len(remaining)}")

    db.disconnect()
    logger.info("Database example completed")


if __name__ == "__main__":
    main()
