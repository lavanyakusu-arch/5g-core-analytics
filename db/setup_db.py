"""
Database setup and connection utilities for the
5G Core Analytics & Insights Platform.
"""

import sqlite3
import logging

logger = logging.getLogger(__name__)


def setup_database(db_path = "db/5g_kpis.db"):
    """
    Create required KPI tables if they do not already exist.

    Args:
        db_path (str): Path to the SQLite database file.
    """
    logger.info("Initializing database at %s", db_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # AMF KPIs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS amf_kpis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            kpi_name TEXT NOT NULL,
            kpi_value REAL NOT NULL
        )
    """)

    # SMF KPIs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS smf_kpis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            kpi_name TEXT NOT NULL,
            kpi_value REAL NOT NULL
        )
    """)

    # SNSSAI / Slice-level KPIs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS snssai_kpis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            nf_type TEXT NOT NULL,
            kpi_name TEXT NOT NULL,
            kpi_value REAL NOT NULL,
            slice TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

    logger.info("Database tables created successfully")


def get_db_connection(db_path: str = "db/5g_kpis.db"):
    """
    Create and return a SQLite database connection.

    Args:
        db_path (str): Path to the SQLite database file.

    Returns:
        sqlite3.Connection: SQLite connection with row factory enabled.
    """
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    return connection
