from datetime import datetime, timedelta
import uuid

def write_log(f, ts, level, proc_id, step, seq, supi, pdu_id, dnn, snssai, result, latency, cause=None):
    log = (
        f"{ts.isoformat()} SMF {level} PDU_SESSION_EST "
        f"proc_id={proc_id} step={step} step_seq={seq} "
        f"supi={supi} pdu_id={pdu_id} dnn={dnn} snssai={snssai} "
        f"result={result}"
    )
    if cause:
        log += f" cause={cause}"
    log += f" latency={latency}ms\n"
    f.write(log)

def generate_success_flow(f, snssai="1-010203"):
    proc_id = f"SMF-PDU-{uuid.uuid4().hex[:8]}"
    supi = "imsi-001010000001234"
    pdu_id = 1
    dnn = "internet"

    steps = [
        "SM_CONTEXT_CREATE_REQUEST",
        "SM_POLICY_ASSOCIATION_REQUEST",
        "SM_POLICY_ASSOCIATION_RESPONSE",
        "PFCP_SESSION_EST_REQUEST",
        "PFCP_SESSION_EST_RESPONSE",
        "PDU_SESSION_EST_COMPLETE"
    ]

    ts = datetime.now()

    for seq, step in enumerate(steps, start=1):
        latency = 10 + seq * 2
        ts += timedelta(milliseconds=latency)

        write_log(
            f, ts, "INFO", proc_id, step, seq,
            supi, pdu_id, dnn, snssai,
            "SUCCESS", latency
        )

def generate_pfcp_failure_flow(f):
    proc_id = f"SMF-PDU-{uuid.uuid4().hex[:8]}"
    supi = "imsi-001010000009999"
    pdu_id = 1
    dnn = "internet"
    snssai = "1-010203"

    steps = [
        "SM_CONTEXT_CREATE_REQUEST",
        "SM_POLICY_ASSOCIATION_REQUEST",
        "SM_POLICY_ASSOCIATION_RESPONSE",
        "PFCP_SESSION_EST_REQUEST",
        "PFCP_SESSION_EST_FAILURE",
        "PDU_SESSION_EST_REJECT"
    ]

    ts = datetime.now()

    for seq, step in enumerate(steps, start=1):
        latency = 10 + seq * 2
        ts += timedelta(milliseconds=latency)

        if step == "PFCP_SESSION_EST_FAILURE" or step == "PFCP_SESSION_EST_REJECT":
            write_log(
                f, ts, "ERROR", proc_id, step, seq,
                supi, pdu_id, dnn, snssai,
                "FAILURE", latency,
                cause="PFCP_TIMEOUT"
            )
        else:
            write_log(
                f, ts, "INFO", proc_id, step, seq,
                supi, pdu_id, dnn, snssai,
            "SUCCESS", latency)

def generate_policy_association_failure_flow(f):
    proc_id = f"SMF-PDU-{uuid.uuid4().hex[:8]}"
    supi = "imsi-001010000009999"
    pdu_id = 1
    dnn = "internet"
    snssai = "1-010203"

    steps = [
        "SM_CONTEXT_CREATE_REQUEST",
        "SM_POLICY_ASSOCIATION_REQUEST",
        "SM_POLICY_ASSOCIATION_FAILURE",
        "PDU_SESSION_EST_REJECT"
    ]

    ts = datetime.now()

    for seq, step in enumerate(steps, start=1):
        latency = 10 + seq * 2
        ts += timedelta(milliseconds=latency)

        if step == "SM_POLICY_ASSOCIATION_FAILURE" or step == "PFCP_SESSION_EST_REJECT":
            write_log(
                f, ts, "ERROR", proc_id, step, seq,
                supi, pdu_id, dnn, snssai,
                "FAILURE", latency,
                cause="POLICY_ASSOCIATION_FAILURE"
            )
        else:
            write_log(
                f, ts, "INFO", proc_id, step, seq,
                supi, pdu_id, dnn, snssai,
            "SUCCESS", latency
            )


def generate_logs(filename):
    with open(filename, "w") as f:
        for _ in range(145):
            generate_success_flow(f, snssai="1-010203")

        for _ in range(32):
            generate_pfcp_failure_flow(f)

        for _ in range(58):
            generate_success_flow(f, snssai="2-020304")

        for _ in range(45):
            generate_policy_association_failure_flow(f)

        for _ in range(43):
            generate_success_flow(f, snssai="3-030405")

if __name__ == "__main__":
    generate_logs("smf.log")

    print("Deterministic procedure-flow logs generated.")
