import sqlite3


def create_db(db_path: str = "demo-db.sqlite") -> None:
    """
    Create a fresh demo SQLite database with tables for users, claims,
    sessions, messages, and knowledge base docs.

    Existing tables are dropped for reproducibility in demo runs.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Drop tables if they already exist
    cursor.executescript("""
    DROP TABLE IF EXISTS session;
    DROP TABLE IF EXISTS claim;
    DROP TABLE IF EXISTS message;
    DROP TABLE IF EXISTS doc;
    DROP TABLE IF EXISTS user;
    """)

    # Create schema
    cursor.executescript("""
    CREATE TABLE user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE,
        profile_data TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE claim (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT NOT NULL,
        problem TEXT,
        solution TEXT,
        status TEXT CHECK(status IN ('Pending', 'Resolved', 'Rejected')) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES user(id)
    );

    CREATE TABLE session (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        ended_at TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES user(id)
    );
    
    CREATE TABLE message (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id INTEGER,
        sender TEXT CHECK(sender IN ('user','assistant', 'tool')) NOT NULL,
        content JSON NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(session_id) REFERENCES session(session_id)
    );
    
    CREATE TABLE doc (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic TEXT,
        question TEXT NOT NULL,
        answer TEXT NOT NULL
    );
    """)

    conn.commit()
    conn.close()


def generate_data(db_path: str = "demo-db.sqlite") -> None:
    """
    Populate the demo database with initial data:
    - 3 users (Alice, Bob, Charlie)
    - Claims for Charlie (one pending, one resolved)
    - Example FAQ document
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Insert users
    users = [
        ("Alice", "alice@example.com", '{"age": 30, "location": "Seattle"}'),
        ("Bob", "bob@example.com", '{"age": 25, "location": "New York"}'),
        ("Charlie", "charlie@example.com", '{"age": 40, "location": "Chicago"}'),
    ]

    cursor.executemany(
        "INSERT INTO user (name, email, profile_data) VALUES (?, ?, ?)", users
    )

    # Map user names to IDs
    cursor.execute("SELECT id, name FROM user")
    user_ids = {name: uid for uid, name in cursor.fetchall()}

    # Insert claims for Charlie
    claims = [
        (
            user_ids["Charlie"],
            "Car Accident Claim",
            "User was involved in a minor car accident and submitted documents.",
            None,
            "Pending",
        ),
        (
            user_ids["Charlie"],
            "Laptop Damage Claim",
            "Laptop stopped working after water damage.",
            "Claim approved. User received reimbursement of $800.",
            "Resolved",
        ),
    ]

    cursor.executemany(
        "INSERT INTO claim (user_id, title, problem, solution, status) VALUES (?, ?, ?, ?, ?)",
        claims,
    )

    # Insert demo docs
    docs = [
        (
            "general",
            "How do I submit a claim?",
            "To submit a claim, log in to the insurance portal, go to 'New Claim', "
            "and upload required documents (ID, photos, receipts).",
        ),
        (
            "general",
            "What documents are needed for car accident claims?",
            "For car accident claims, you need to provide a police report, "
            "photos of the damage, and repair estimates.",
        ),
        (
            "general",
            "How can I check the status of my claim?",
            "You can check claim status online via the portal or "
            "contact support with your claim ID.",
        ),
        (
            "general",
            "What is covered under home insurance?",
            "Home insurance typically covers fire, theft, and water damage. "
            "Flooding may require additional coverage.",
        ),
        (
            "general",
            "What should I do if I cannot submit a claim online?",
            "If you experience issues submitting a claim online, "
            "please contact support or visit a local branch.",
        ),
        (
            "general",
            "How long does it take to process a claim?",
            "Processing time is usually 5–10 business days depending on "
            "claim type and documentation completeness.",
        ),
    ]

    cursor.executemany(
        "INSERT INTO doc (topic, question, answer) VALUES (?, ?, ?)", docs
    )

    conn.commit()
    conn.close()


def main():
    """Recreate the demo DB with example data."""
    create_db(db_path="demo-db.sqlite")
    generate_data(db_path="demo-db.sqlite")


if __name__ == "__main__":
    main()
