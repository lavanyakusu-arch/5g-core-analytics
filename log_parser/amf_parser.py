import re

def parse_amf_logs(lines):
    kpis = {
        "registration_request": 0,
        "registration_success": 0,
        "authentication_request": 0,
        "authentication_success": 0,
        "authentication_failure": 0,
        "authentication_retry": 0,
        "registration_reject": 0
    }

    regex_map = {
        r"registration_request": "registration_request",
        r"registration_complete": "registration_success",
        r"authentication_request": "authentication_request",
        r"authentication_success": "authentication_success",
        r"authentication_failure": "authentication_failure",
        r"authentication_retry": "authentication_retry",
        r"registration_reject": "registration_reject"
    }

    for line in lines:
        for pattern, key in regex_map.items():
            if re.search(pattern, line):
                kpis[key] += 1
                break

    return kpis