import logging
from db.setup_db import get_db_connection

logger = logging.getLogger(__name__)

def fetch_nssai_kpis():
    logger.info("Fetching NSSAI KPIs from database")

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT slice, SUM(value) AS total_sessions
            FROM snssai_kpis
            WHERE kpi_name = 'snssai_ue_count'
            GROUP BY slice
        """)

        rows = cursor.fetchall()
        logger.debug("Raw NSSAI rows fetched: %s", rows)

        # SST → Slice type mapping (3GPP)
        slice_map = {
            1: "eMBB",
            2: "URLLC",
            3: "mMTC"
        }

        result = {}

        for slice_value, count in rows:
            sst = int(slice_value.split("-")[0])
            slice_name = slice_map.get(sst, f"Unknown(SST={sst})")

            result[slice_name] = {
                "sessions": count,
                "nssai": slice_value
            }

        logger.info("Processed NSSAI KPIs for %d slices", len(result))
        logger.debug("Final NSSAI KPI result: %s", result)

        return result

    except Exception:
        logger.exception("Failed to fetch NSSAI KPIs")
        raise

    finally:
        conn.close()
        logger.debug("Database connection closed after NSSAI KPI fetch")
