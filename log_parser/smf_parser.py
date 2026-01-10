import re
from collections import defaultdict

def parse_smf_logs(lines):
    kpis = {
        "pdu_session_create_request":0,
        "pfcp_session_establishment_request":0,
        "pfcp_session_establishment_failure":0,
        "pfcp_session_establishment_response":0,
        "policy_association_request":0,
        "policy_association_response":0,
        "policy_association_failure":0,
        "pdu_session_est_complete":0,
        "pdu_session_est_reject":0
    }
    snssai_counter=defaultdict(int)

    regex_map = {
        r"SM_CONTEXT_CREATE_REQUEST": "pdu_session_create_request",
        r"SM_POLICY_ASSOCIATION_REQUEST": "policy_association_request",
        r"SM_POLICY_ASSOCIATION_RESPONSE": "policy_association_response",
        r"PFCP_SESSION_EST_REQUEST": "pfcp_session_establishment_request",
        r"PFCP_SESSION_EST_RESPONSE": "pfcp_session_establishment_response",
        r"PDU_SESSION_EST_COMPLETE": "pdu_session_est_complete",
        r"PDU_SESSION_EST_REJECT": "pdu_session_est_reject",
        r"PFCP_SESSION_EST_FAILURE": "pfcp_session_establishment_failure",
        r"SM_POLICY_ASSOCIATION_FAILURE": "policy_association_failure",
    }

    for line in lines:
        for pattern, key in regex_map.items():
            match = re.search(pattern, line)
            if match:
                kpis[key] += 1
            if key == "pdu_session_est_complete":
                match_snssai = re.search(r"snssai=(\d+-[0-9A-Fa-f]+)", line)
                if match_snssai:
                    snssai = match_snssai.group(1)
                    snssai_counter[snssai] += 1

    return kpis, snssai_counter
