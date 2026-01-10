import logging
import sqlite3
from db.setup_db import get_db_connection

logger = logging.getLogger(__name__)

def fetch_amf_kpis():
    logger.info("Fetching AMF KPIs from database")

    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT kpi_name, SUM(kpi_value) AS value
            FROM amf_kpis
            GROUP BY kpi_name
        """)

        rows = cursor.fetchall()
        amf = {row["kpi_name"]: row["value"] for row in rows}

        logger.debug("AMF KPI raw data: %s", amf)

        return {
            "registration_request": amf.get("registration_request", 0),
            "registration_success": amf.get("registration_success", 0),
            "registration_reject": amf.get("registration_reject", 0),
            "authentication_request": amf.get("authentication_request", 0),
            "authentication_success": amf.get("authentication_success", 0),
            "authentication_failure": amf.get("authentication_failure", 0),
            "authentication_retry": amf.get("authentication_retry", 0)
        }

    except Exception:
        logger.exception("Failed to fetch AMF KPIs")
        raise

    finally:
        conn.close()
        logger.debug("Database connection closed after AMF KPI fetch")