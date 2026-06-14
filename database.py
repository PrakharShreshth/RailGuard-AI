import sqlite3
import pandas as pd

DB_NAME = "railguard.db"


def create_table():

    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS detections(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        defect TEXT,
        confidence REAL,
        risk_level TEXT,
        risk_score INTEGER
    )
    """)

    conn.commit()
    conn.close()


def insert_detection(
    defect,
    confidence,
    risk_level,
    risk_score
):

    conn = sqlite3.connect(DB_NAME)

    conn.execute(
        """
        INSERT INTO detections
        (
            defect,
            confidence,
            risk_level,
            risk_score
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            defect,
            confidence,
            risk_level,
            risk_score
        )
    )

    conn.commit()
    conn.close()


def get_all_detections():

    conn = sqlite3.connect(DB_NAME)

    query = """
    SELECT *
    FROM detections
    ORDER BY id DESC
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df
