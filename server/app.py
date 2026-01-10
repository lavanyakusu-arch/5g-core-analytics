import logging
from fastapi import FastAPI
from db.db_summary import get_kpi_summary_from_db
from db.amf_kpis import fetch_amf_kpis
from db.smf_kpis import fetch_smf_kpis
from db.nssai_kpis import fetch_nssai_kpis
from server.amf_kpi_calculator import calculate_amf_rates
from server.smf_kpi_calculator import calculate_smf_rates

# -------------------- Logging --------------------
logger = logging.getLogger("5g_core_api")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)

# -------------------- FastAPI --------------------
app = FastAPI(title="5G Core Analytics API")

@app.get("/summary")
def summary():
    logger.info("Request received: /summary")
    try:
        data = get_kpi_summary_from_db()
        return data
    except Exception:
        logger.exception("Failed to fetch summary")
        return {"error": "Failed to fetch KPI summary"}

@app.get("/amf")
def get_amf_metrics():
    logger.info("Request received: /amf")
    try:
        kpis = fetch_amf_kpis()
        if not kpis:
            logger.warning("No AMF KPI data available")
            return {"message": "No AMF KPI data available"}

        rates = calculate_amf_rates(kpis)
        return {"kpis": kpis, "rates": rates}
    except Exception:
        logger.exception("Failed to fetch AMF KPIs")
        return {"error": "Failed to fetch AMF KPI data"}

@app.get("/smf")
def get_smf_metrics():
    logger.info("Request received: /smf")
    try:
        kpis = fetch_smf_kpis()
        if not kpis:
            logger.warning("No SMF KPI data available")
            return {"message": "No SMF KPI data available"}

        rates = calculate_smf_rates(kpis)
        return {"kpis": kpis, "rates": rates}
    except Exception:
        logger.exception("Failed to fetch SMF KPIs")
        return {"error": "Failed to fetch SMF KPI data"}

@app.get("/snssai")
def get_snssai_metrics():
    logger.info("Request received: /snssai")
    try:
        return fetch_nssai_kpis()
    except Exception:
        logger.exception("Failed to fetch NSSAI KPIs")
        return {"error": "Failed to fetch NSSAI KPI data"}
