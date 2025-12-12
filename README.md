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

## 📂 **Project Structure**

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

## 🔧 **Prerequisites**

Install the following:

* Docker
* Docker Compose
* Alpha Vantage API Key: [https://www.alphavantage.co/support/#api-key](https://www.alphavantage.co/support/#api-key)

---

## ⚙️ **Setup Instructions**

### **1. Clone the project**

```bash
git clone https://github.com/syedsami1/docker-airflow-stock-pipeline.git
cd Stock-pipeline
```

---

### **2. Configure environment variables**

Edit the `.env` file:

```
POSTGRES_USER=airflow
POSTGRES_PASSWORD=airflow
POSTGRES_DB=stocks_db
ALPHA_VANTAGE_API_KEY=YOUR_API_KEY_HERE
```

---

### **3. Start Docker Desktop**

Ensure Docker Desktop is running before continuing.

---

### **4. Build and run the entire pipeline**

```bash
docker-compose up --build
```

This command will:

* Start PostgreSQL
* Initialize Airflow
* Install dependencies
* Launch scheduler + webserver

Airflow UI → [http://localhost:8080](http://localhost:8080)

---

### **5. Log into Airflow**

Default credentials:

```
Username: admin
Password: admin
```

---

### **6. Enable & Trigger the DAG**

In Airflow UI, switch **ON** the DAG:

```
stock_data_pipeline
```

To trigger manually via CLI:

```bash
docker exec -it stock_pipeline-airflow-webserver-1 \
airflow dags trigger stock_data_pipeline
```

---

## 🧠 **Pipeline Workflow**

### **1️⃣ Airflow DAG (`stock_data_dag.py`)**

* Runs daily
* Triggers `fetch_and_store.py` using a BashOperator
* Ensures task is robust to API failures

---

### **2️⃣ Data Fetching (`fetch_and_store.py`)**

The script:

1. Calls Alpha Vantage API

2. Validates JSON response

3. Extracts:

   * date
   * open
   * high
   * low
   * close
   * volume

4. Returns cleaned data

Includes `try/except` blocks for error handling.

---

### **3️⃣ Data Storage in PostgreSQL**

The script:

* Connects to PostgreSQL
* Creates the `stock_prices` table if it does not exist
* Performs UPSERT with:

```sql
ON CONFLICT (date) DO UPDATE
```

Ensures the latest stock data is always stored.

---

## 📊 **Database Schema**

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

## ✅ **Example Database Output**

After running the DAG:

```sql
stocks_db=# SELECT * FROM stock_prices ORDER BY date DESC;
    date    |  open   |  high  |  low   | close  |  volume
------------+---------+--------+--------+--------+----------
 2025-12-11 | 279.095 | 279.59 | 273.81 | 278.03 | 33247986
(1 row)
```

---

## 🛠 **Stopping the pipeline**

```bash
docker-compose down
```

To remove the database volume:

```bash
docker-compose down -v
```

---

## 🔍 **Troubleshooting**

### Docker engine not running?

Error message:

```
open //./pipe/dockerDesktopLinuxEngine: file not found
```

→ Start **Docker Desktop**.

---

## 🧩 **Optional Improvements**

* Replace BashOperator with PythonOperator
* Add logging module instead of print
* Fetch historical stock data
* Add unit tests to verify database insertion and API output

