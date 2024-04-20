import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv

load_dotenv()


# Connect to the new database and create a table
conn = psycopg2.connect(
    dbname=os.getenv("PGDATABASE"),
    user=os.getenv("PGUSER"),
    password=os.getenv("PGPASSWORD"),
    host=os.getenv("PGHOST")
)

cur = conn.cursor()
# Check if the table exists
cur.execute("""
    SELECT to_regclass('public.chrome_web_store_item')
""")

# If it doesn't exist, create it
if cur.fetchone()[0] is None:
    cur.execute("""
        CREATE TABLE chrome_web_store_item (
            id TEXT PRIMARY KEY,
            url TEXT,
            title TEXT,
            icon TEXT,
            small_promo_tile TEXT,
            website_owner TEXT,
            created_by_the_website_owner BOOLEAN,
            featured BOOLEAN,
            rating DECIMAL,
            rating_count INTEGER,
            type TEXT,
            category TEXT,
            users INTEGER,
            screenshots TEXT[],
            overview TEXT,
            version TEXT,
            size TEXT,
            languages TEXT[],
            last_updated INTEGER,
            developer JSONB
        )
    """)

    # Commit the transaction
    conn.commit()

    print("Table chrome_web_store_item created successfully")
else:
    print("Table chrome_web_store_item already exists")

# Close the cursor and connection
cur.close()
conn.close()
