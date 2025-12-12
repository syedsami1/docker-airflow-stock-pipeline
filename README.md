
# **Stock Market Data Pipeline (Airflow + Docker + PostgreSQL)**

This project implements a fully Dockerized data pipeline that automatically fetches stock market data from the **Alpha Vantage API**, processes it, and stores it into a **PostgreSQL database** using **Apache Airflow** as the orchestrator.

---

## 🚀 **Features**

* Automated daily data ingestion
* JSON parsing & transformation
* PostgreSQL table creation + UPSERT logic
* Robust error handling
* Environment-based credentials
* Fully containerized (Docker Compose)

---

# 📂 **Project Structure**

```
Stock-pipeline/
│
├── airflow/
│   ├── dags/
│   │   └── stock_data_dag.py
│   └── requirements.txt
│
├── scripts/
│   └── fetch_and_store.py
│
├── .env
├── docker-compose.yml
└── README.md
```

---

# 🔧 **Prerequisites**

Install the following:

* Docker
* Docker Compose
* Alpha Vantage API Key (free): [https://www.alphavantage.co/support/#api-key](https://www.alphavantage.co/support/#api-key)

---

# ⚙️ **Setup Instructions**

## **1. Clone the project**

```bash
git clone <your-repo-url>
cd Stock-pipeline
```

---

## **2. Configure environment variables**

Edit the `.env` file:

```
POSTGRES_USER=airflow
POSTGRES_PASSWORD=airflow
POSTGRES_DB=stocks_db
ALPHA_VANTAGE_API_KEY=YOUR_API_KEY_HERE
```

---

## **3. Start Docker Desktop**

Make sure Docker Desktop is **running** before continuing.

---

## **4. Build and run the entire pipeline**

```bash
docker-compose up --build
```

This command:

* Starts PostgreSQL
* Initializes Airflow
* Installs dependencies
* Launches scheduler + webserver

Airflow UI → [http://localhost:8080](http://localhost:8080)

---

## **5. Log into Airflow**

Default credentials:

```
Username: admin
Password: admin
```

---

## **6. Enable the DAG**

In Airflow UI, switch **ON**:

```
stock_data_pipeline
```

You can also trigger it manually.

---

# 🧠 **Pipeline Workflow**

## **1️⃣ Airflow DAG (`stock_data_dag.py`)**

* Runs daily
* Triggers `fetch_and_store.py` using a BashOperator

---

## **2️⃣ Data Fetching (`fetch_and_store.py`)**

The script:

1. Calls Alpha Vantage API
2. Validates JSON
3. Extracts:

   * date
   * open
   * high
   * low
   * close
   * volume
4. Returns cleaned data

Includes `try/except` for API errors.

---

## **3️⃣ Data Storage in PostgreSQL**

The script:

* Connects to PostgreSQL
* Creates table if not exists
* Performs UPSERT using:

```sql
ON CONFLICT (date) DO UPDATE
```

Ensures the latest data is always stored.

---

# 📊 **Database Schema**

```sql
CREATE TABLE stock_prices (
  date DATE PRIMARY KEY,
  open FLOAT,
  high FLOAT,
  low FLOAT,
  close FLOAT,
  volume BIGINT
);
```

---

# 🛠 **Stopping the pipeline**

```bash
docker-compose down
```

Remove database volume:

```bash
docker-compose down -v
```

---

# 🔍 **Troubleshooting**

### **Docker engine not running?**

If you see:

```
open //./pipe/dockerDesktopLinuxEngine: file not found
```

→ You must start **Docker Desktop**.

---

# 🧩 **Optional Improvements**

* Replace BashOperator with PythonOperator
* Add logging module instead of print
* Add historical data fetching
* Add unit tests
