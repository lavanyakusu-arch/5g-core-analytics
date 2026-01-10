import logging

logger = logging.getLogger(__name__)

def calculate_smf_rates(data):
    logger.info("Calculating SMF KPI success/failure rates")
    try:
        session_success = data.get("pdu_session_establishment_complete", 0)
        session_reject = data.get("pdu_session_establishment_reject", 0)

        policy_success = data.get("sm_policy_association_response", 0)
        policy_failure = data.get("sm_policy_association_failure", 0)

        pfcp_success = data.get("pfcp_session_establishment_response", 0)
        pfcp_failure = data.get("pfcp_session_establishment_failure", 0)

        total_session = session_success + session_reject
        total_policy = policy_success + policy_failure
        total_pfcp = pfcp_success + pfcp_failure

        rates = {
            "PDU Session Establishment Success Rate": round((session_success / total_session) * 100, 2) if total_session else 0,
            "PDU Session Establishment Failure Rate": round((session_reject / total_session) * 100, 2) if total_session else 0,
            "SM Policy Association Success Rate": round((policy_success / total_policy) * 100, 2) if total_policy else 0,
            "SM Policy Association Failure Rate": round((policy_failure / total_policy) * 100, 2) if total_policy else 0,
            "PFCP Session Success Rate": round((pfcp_success / total_pfcp) * 100, 2) if total_pfcp else 0,
            "PFCP Session Failure Rate": round((pfcp_failure / total_pfcp) * 100, 2) if total_pfcp else 0,
        }

        logger.debug("SMF KPI rates calculated: %s", rates)
        return rates

    except Exception:
        logger.exception("Failed to calculate SMF KPI rates")
        raise
