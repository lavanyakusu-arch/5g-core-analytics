"""
KPI insertion utilities for the
5G Core Analytics & Insights Platform.
"""

from datetime import datetime
import logging
from typing import Dict

from db.setup_db import get_db_connection

logger = logging.getLogger(__name__)


def insert_amf_kpis(amf_kpis: Dict[str, float], db_path: str = "db/5g_kpis.db"):
    """
    Insert AMF KPIs into the database.
    """
    logger.info("Inserting AMF KPIs: %s", amf_kpis)

    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    timestamp = datetime.utcnow().isoformat()

    try:
        for kpi_name, kpi_value in amf_kpis.items():
            cursor.execute(
                """
                INSERT INTO amf_kpis (timestamp, kpi_name, kpi_value)
                VALUES (?, ?, ?)
                """,
                (timestamp, kpi_name, kpi_value)
            )

        conn.commit()
        logger.info("AMF KPIs inserted successfully")

    except Exception as exc:
        conn.rollback()
        logger.exception("Failed to insert AMF KPIs: %s", exc)
        raise

    finally:
        conn.close()


def insert_smf_kpis(smf_kpis: Dict[str, float], db_path: str = "db/5g_kpis.db"):
    """
    Insert SMF KPIs into the database.
    """
    logger.info("Inserting SMF KPIs: %s", smf_kpis)

    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    timestamp = datetime.utcnow().isoformat()

    try:
        for kpi_name, kpi_value in smf_kpis.items():
            cursor.execute(
                """
                INSERT INTO smf_kpis (timestamp, kpi_name, kpi_value)
                VALUES (?, ?, ?)
                """,
                (timestamp, kpi_name, kpi_value)
            )

        conn.commit()
        logger.info("SMF KPIs inserted successfully")

    except Exception as exc:
        conn.rollback()
        logger.exception("Failed to insert SMF KPIs: %s", exc)
        raise

    finally:
        conn.close()


def insert_nssai_kpis(
    nf: str,
    nssai_kpis: Dict[str, int],
    db_path: str = "db/5g_kpis.db"):
    """
    Insert slice-level (SNSSAI) KPIs into the database.
    """
    logger.info("Inserting SNSSAI KPIs for NF: %s", nf)

    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    timestamp = datetime.utcnow().isoformat()

    try:
        for slice_id, ue_count in nssai_kpis.items():
            cursor.execute(
                """
                INSERT INTO snssai_kpis
                (timestamp, nf, kpi_name, value, slice)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    timestamp,
                    nf,
                    "snssai_ue_count",
                    ue_count,
                    slice_id
                )
            )

        conn.commit()
        logger.info("SNSSAI KPIs inserted successfully")

    except Exception as exc:
        conn.rollback()
        logger.exception("Failed to insert SNSSAI KPIs: %s", exc)
        raise

    finally:
        conn.close()
