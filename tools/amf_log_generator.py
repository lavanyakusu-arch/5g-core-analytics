import time
import json
import uuid
import random
from datetime import datetime, timedelta

def generate_registration_with_retry(start_log_id=1, max_retries=1):
    procedure_id = f"reg-{uuid.uuid4().hex[:6]}"
    ue_id = f"imsi-00101{random.randint(100000000, 999999999)}"
    ran_id = f"gnb-{random.randint(100, 199)}"

    base_time = datetime.utcnow()
    logs = []
    log_id = start_log_id
    current_time = base_time

    def add_log(event, result, latency, retry_count=0, error_code=None):
        nonlocal log_id, current_time
        current_time += timedelta(milliseconds=latency)
        logs.append({
            "log_id": log_id,
            "timestamp": current_time.isoformat(),
            "nf_type": "AMF",
            "procedure": "registration",
            "procedure_id": procedure_id,
            "event_name": event,
            "retry_count": retry_count,
            "ue_id": ue_id,
            "supi": ue_id,
            "ran_id": ran_id,
            "result": result,
            "latency_ms": latency,
            "error_code": error_code
        })
        log_id += 1

    # Step 1: Registration Request
    add_log("registration_request", "SUCCESS", latency=6)

    # Step 2: Authentication Request
    add_log("authentication_request", "SUCCESS", latency=random.randint(10, 18))

    # Step 3: Authentication Failure(s)
    for retry in range(1, max_retries + 1):
        add_log(
            event="authentication_failure",
            result="FAILURE",
            latency=random.randint(8, 15),
            retry_count=retry,
            error_code="AUTH_REJECT"
        )
        add_log(
            event="authentication_retry",
            result="RETRY",
            latency=random.randint(3, 6),
            retry_count=retry
        )

    # Step 4: Authentication Success
    add_log("authentication_success", "SUCCESS", latency=random.randint(10, 18))

    # Step 5: Registration Complete
    add_log("registration_complete", "SUCCESS", latency=random.randint(5, 10))

    return logs

def generate_registration_success(start_log_id=1):
    procedure_id = f"reg-{uuid.uuid4().hex[:6]}"
    ue_id = f"imsi-00101{random.randint(100000000, 999999999)}"
    ran_id = f"gnb-{random.randint(100, 199)}"

    base_time = datetime.utcnow()
    logs = []
    log_id = start_log_id
    current_time = base_time

    def add_log(event, result, latency, retry_count=0, error_code=None):
        nonlocal log_id, current_time
        current_time += timedelta(milliseconds=latency)
        logs.append({
            "log_id": log_id,
            "timestamp": current_time.isoformat(),
            "nf_type": "AMF",
            "procedure": "registration",
            "procedure_id": procedure_id,
            "event_name": event,
            "retry_count": retry_count,
            "ue_id": ue_id,
            "supi": ue_id,
            "ran_id": ran_id,
            "result": result,
            "latency_ms": latency,
            "error_code": error_code
        })
        log_id += 1

    # Step 1: Registration Request
    add_log("registration_request", "SUCCESS", latency=6)

    # Step 2: Authentication Request
    add_log("authentication_request", "SUCCESS", latency=random.randint(10, 18))

    # Step 3: Authentication Success
    add_log("authentication_success", "SUCCESS", latency=random.randint(10, 18))

    # Step 4: Registration Complete
    add_log("registration_complete", "SUCCESS", latency=random.randint(5, 10))

    return logs

def generate_registration_reject(start_log_id=1):
    procedure_id = f"reg-{uuid.uuid4().hex[:6]}"
    ue_id = f"imsi-00101{random.randint(100000000, 999999999)}"
    ran_id = f"gnb-{random.randint(100, 199)}"

    base_time = datetime.utcnow()
    logs = []
    log_id = start_log_id
    current_time = base_time

    def add_log(event, result, latency, retry_count=0, error_code=None):
        nonlocal log_id, current_time
        current_time += timedelta(milliseconds=latency)
        logs.append({
            "log_id": log_id,
            "timestamp": current_time.isoformat(),
            "nf_type": "AMF",
            "procedure": "registration",
            "procedure_id": procedure_id,
            "event_name": event,
            "retry_count": retry_count,
            "ue_id": ue_id,
            "supi": ue_id,
            "ran_id": ran_id,
            "result": result,
            "latency_ms": latency,
            "error_code": error_code
        })
        log_id += 1

    # Step 1: Registration Request
    add_log("registration_request", "SUCCESS", latency=6)

    # Step 2: Authentication Request
    add_log("registration_reject", "FAILURE", latency=random.randint(10, 18))

    return logs

def write_logs(logs, filename="amf.log"):
    with open(filename, "a") as f:
        for log in logs:
            f.write(json.dumps(log) + "\n")

    print(f"Generated {len(logs)} logs → {filename}")

if __name__ == "__main__":

    for _ in range(165):
        success_logs = generate_registration_success()
        write_logs(success_logs)

    for _ in range(78):
        auth_failure_logs = generate_registration_with_retry(max_retries=2)
        write_logs(auth_failure_logs)

    for _ in range(63):
        success_logs1 = generate_registration_success()
        write_logs(success_logs1)

    for _ in range(10):
        reg_reject_logs1 = generate_registration_reject()
        write_logs(reg_reject_logs1)





