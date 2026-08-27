import sqlite3

connection = sqlite3.connect("xrp_bot.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS price_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    xrp_usd REAL,
    usd_aud REAL,
    xrp_aud REAL
)
""")

connection.commit()
connection.close()

print("Database created!")