"""
Main entry point for the 5G Core Analytics & Insights Platform.

Responsibilities:
- Read AMF and SMF logs
- Parse KPIs from logs
- Initialize database schema
- Persist KPIs into the database
"""

import logging

from log_parser.log_reader import read_log
from log_parser.amf_parser import parse_amf_logs
from log_parser.smf_parser import parse_smf_logs

from db.setup_db import setup_database
from db.insert_kpis import (
    insert_amf_kpis,
    insert_smf_kpis,
    insert_nssai_kpis
)


# ---------------- Configuration ----------------
AMF_LOG_PATH = "logs/amf.log"
SMF_LOG_PATH = "logs/smf.log"
DB_PATH = "db/5g_kpis.db"


# ---------------- Logging Setup ----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """
    Execute the KPI ingestion and persistence workflow.
    """
    logger.info("Starting 5G Core Analytics pipeline")

    # Initialize database
    setup_database(db_path=DB_PATH)
    logger.info("Database initialized successfully")

    # Read log files
    amf_log_lines = read_log(AMF_LOG_PATH)
    smf_log_lines = read_log(SMF_LOG_PATH)
    logger.info("Log files loaded (AMF=%d lines, SMF=%d lines)",
                len(amf_log_lines), len(smf_log_lines))

    # Parse KPIs
    amf_kpis = parse_amf_logs(amf_log_lines)
    smf_kpis, nssai_kpis = parse_smf_logs(smf_log_lines)

    logger.info("Parsed AMF KPIs: %s", amf_kpis)
    logger.info("Parsed SMF KPIs: %s", smf_kpis)
    logger.info("Parsed NSSAI KPIs: %s", nssai_kpis)

    # Persist KPIs
    insert_amf_kpis(amf_kpis)
    insert_smf_kpis(smf_kpis)
    insert_nssai_kpis(nf="SMF", nssai_kpis=nssai_kpis)

    logger.info("All KPIs successfully stored in database")
    logger.info("5G Core Analytics pipeline completed")


if __name__ == "__main__":
    main()
