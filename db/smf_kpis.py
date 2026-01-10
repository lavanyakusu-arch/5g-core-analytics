import logging
import sqlite3
from db.setup_db import get_db_connection

logger = logging.getLogger(__name__)

def fetch_smf_kpis():
    logger.info("Fetching SMF KPIs from database")

    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT kpi_name, SUM(kpi_value) AS value
            FROM smf_kpis
            GROUP BY kpi_name
        """)

        rows = cursor.fetchall()
        smf = {row["kpi_name"]: row["value"] for row in rows}

        logger.debug("SMF KPI raw data: %s", smf)

        return {
            "pdu_session_establishment_request": smf.get("pdu_session_create_request", 0),
            "sm_policy_association_request": smf.get("policy_association_request", 0),
            "sm_policy_association_response": smf.get("policy_association_response", 0),
            "sm_policy_association_failure": smf.get("policy_association_failure", 0),
            "pfcp_session_establishment_request": smf.get("pfcp_session_establishment_request", 0),
            "pfcp_session_establishment_response": smf.get("pfcp_session_establishment_response", 0),
            "pdu_session_establishment_complete": smf.get("pdu_session_est_complete", 0),
            "pdu_session_establishment_reject": smf.get("pdu_session_est_reject", 0),
            "pfcp_session_establishment_failure": smf.get("pfcp_session_establishment_failure", 0)
        }

    except Exception:
        logger.exception("Failed to fetch SMF KPIs")
        raise

    finally:
        conn.close()
        logger.debug("Database connection closed after SMF KPI fetch")
