import sqlite3

# setup a malicious db
conn = sqlite3.connect("malicious.db")
c = conn.cursor()
c.execute("CREATE TABLE 'malicious\"; DROP TABLE users; --' (id int)")
c.execute("INSERT INTO 'malicious\"; DROP TABLE users; --' VALUES (1)")
conn.commit()
conn.close()

from pathlib import Path

from src.ingestion.sql_loader import load_sql

# Try to find a way to inject
print(load_sql(Path("malicious.db")))
