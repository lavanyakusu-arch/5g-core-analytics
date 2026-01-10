import logging
import sqlite3
from db.setup_db import get_db_connection

logger = logging.getLogger(__name__)

def get_kpi_summary_from_db():
    logger.info("Fetching network KPI summary from database")

    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    try:
        # ---------- AMF ----------
        cur.execute("""
            SELECT kpi_name, SUM(kpi_value) as value
            FROM amf_kpis
            GROUP BY kpi_name
        """)
        amf_rows = cur.fetchall()
        amf = {row["kpi_name"]: row["value"] for row in amf_rows}
        logger.debug("AMF raw data: %s", amf)

        reg_req = amf.get("registration_request", 0)
        reg_succ = amf.get("registration_success", 0)
        reg_fail = amf.get("registration_reject", 0)

        # ---------- SMF ----------
        cur.execute("""
            SELECT kpi_name, SUM(kpi_value) as value
            FROM smf_kpis
            GROUP BY kpi_name
        """)
        smf_rows = cur.fetchall()
        smf = {row["kpi_name"]: row["value"] for row in smf_rows}
        logger.debug("SMF raw data: %s", smf)

        pdu_req = smf.get("pdu_session_create_request", 0)
        pdu_succ = smf.get("pdu_session_est_complete", 0)
        pdu_fail = smf.get("pdu_session_est_reject", 0)

        # ---------- Rates ----------
        reg_success_rate = round((reg_succ / reg_req) * 100, 2) if reg_req else 0
        session_success_rate = round((pdu_succ / pdu_req) * 100, 2) if pdu_req else 0

        summary = {
            "registered_ues": reg_succ,
            "pdu_sessions_established": pdu_succ,
            "registration_failures": reg_fail,
            "pdu_session_failures": pdu_fail,
            "registration_success_rate": reg_success_rate,
            "session_success_rate": session_success_rate
        }

        logger.info("Fetched network KPI summary successfully")
        logger.debug("KPI summary: %s", summary)

        return summary

    except Exception:
        logger.exception("Failed to fetch KPI summary")
        raise

    finally:
        conn.close()
        logger.debug("Database connection closed after KPI summary fetch")
