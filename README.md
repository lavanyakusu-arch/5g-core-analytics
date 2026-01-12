# 5G Core Analytics & Insights Platform

A Python-based analytics system that parses **5G Core Network Function (NF) logs**
(AMF, SMF), computes key performance indicators (KPIs), and stores them for
analytics, visualization, and API exposure.

This project simulates the analytics role of **5G NWDAF**, parsing AMF/SMF logs, computing KPIs, and providing insights for network slices.

---
## 🚀 Key Features

- 📡 **AMF KPIs**
  - Registration Requests
  - Registration Success
  - Registration Failure

- 🔗 **SMF KPIs**
  - PDU Session Attempts
  - PDU Session Success

- 🧩 **Slice-Level (SNSSAI) Analytics**
  - Session count per network slice (eMBB, URLLC, etc.)

- 🗄️ **Persistence Layer**
  - SQLite-based KPI storage
  - Clean schema design with extensibility

- 🧱 **Clean Architecture**
  - Log Parsing → KPI Computation → Database
  - Extensible to FastAPI & Streamlit

---

## 🏗️ Architecture Overview

```text
5G NF Logs (AMF / SMF)
        ↓
Log Parser Layer
        ↓
KPI Computation
        ↓
SQLite Database
        ↓
FastAPI (APIs) / Streamlit (Dashboard)
```
## Project Structure

- **log_parser/**: Contains modules to read and parse 5G Core Network Function logs (AMF, SMF) and extract KPIs.
- **tools/**: Contains helper utilities such as log generators for simulating 5G Core NF logs.
- **db/**: Contains database setup, connection utilities, KPI insertion logic, and database-level APIs for storing and fetching KPIs.
- **logs/**: Contains sample AMF and SMF log files used for KPI extraction and testing.
- **server/**: Contains the FastAPI backend code for exposing KPIs and analytics via REST APIs.
- **dashboard/**: Contains the Streamlit application code for visualizing KPIs and network analytics.
- **main.py**: Entry point that orchestrates log parsing, KPI computation, and database storage.
- **requirements.txt**: Lists the required Python packages for the project.
- **README.md**: Provides an overview, architecture description, and usage instructions for the project.

## Setup Instructions

1. **Clone the repository**:
    ```bash
    git clone https://github.com/lavanyakusu-arch/5g-core-analytics.git
    cd 5g-core-analytics
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the main ingestion script**:
    ```bash
    python main.py
    ```
### Sample output:

```text
INFO | Starting 5G Core Analytics pipeline
INFO | Database initialized successfully
INFO | Log files loaded (AMF=1556 lines, SMF=2094 lines)

INFO | Parsed AMF KPIs:
{'registration_request': 316, 'regist0ration_success': 306,'authentication_request': 306, 'authentication_success': 306,'authentication_failure': 156, 'authentication_retry': 156,'registration_reject': 10}

INFO | Parsed SMF KPIs:
{'pdu_session_create_request': 323,'pfcp_session_establishment_request': 278,'pfcp_session_establishment_failure': 32,'pfcp_session_establishment_response': 492,'policy_association_request': 323,'policy_association_response': 278,'policy_association_failure': 45,'pdu_session_est_complete': 246,'pdu_session_est_reject': 77}

INFO | Parsed SNSSAI KPIs:
{'1-010203': 1387, '2-020304': 406, '3-030405': 301}

INFO | All KPIs successfully stored in database
INFO | 5G Core Analytics pipeline completed
```

4. **Run the FastAPI server**:
    ```commandline
    uvicorn server.app:app --reload
    ```
### Sample output:

```text
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

5. **Run the Streamlit app**:
    ```commandline
    streamlit run dashboard/ui_dashboard.py
    ```
### Sample output:
```text
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501

```

## Log Generator (Optional)

The project includes a log generator utility to simulate AMF and SMF logs
for testing and demonstration purposes.

To generate sample logs:
```bash
python tools/log_generator.py
```
