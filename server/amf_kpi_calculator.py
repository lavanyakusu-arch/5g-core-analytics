import logging

logger = logging.getLogger(__name__)

def calculate_amf_rates(data):
    logger.info("Calculating AMF KPI success/failure rates")
    try:
        reg_success = data.get("registration_success", 0)
        reg_reject = data.get("registration_reject", 0)
        auth_success = data.get("authentication_success", 0)
        auth_failure = data.get("authentication_failure", 0)

        total_reg = reg_success + reg_reject
        total_auth = auth_success + auth_failure

        rates = {
            "Registration Success Rate": round((reg_success / total_reg) * 100, 2) if total_reg else 0,
            "Registration Failure Rate": round((reg_reject / total_reg) * 100, 2) if total_reg else 0,
            "Authentication Success Rate": round((auth_success / total_auth) * 100, 2) if total_auth else 0,
            "Authentication Failure Rate": round((auth_failure / total_auth) * 100, 2) if total_auth else 0,
        }

        logger.debug("AMF KPI rates calculated: %s", rates)
        return rates

    except Exception:
        logger.exception("Failed to calculate AMF KPI rates")
        raise
