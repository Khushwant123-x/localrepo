MLOps Batch Signal Pipeline

Overview
This project is a lightweight MLOps-style batch pipeline built using Python. It processes financial OHLCV data, generates trading signals using a rolling mean strategy, and outputs structured metrics with logging and Docker support.

Features:
Config-driven execution using YAML
Reproducible runs using fixed seed
Rolling mean-based feature engineering
Rule-based signal generation
Data validation (missing file, schema check, empty dataset handling)
Structured logging and metrics tracking
Dockerized deployment

Project Structure:
mlops-task/
run.py
config.yaml
data.csv
requirements.txt
Dockerfile
metrics.json
run.log

Workflow:
Load config from config.yaml
Read and validate data.csv
Compute rolling mean on close column
Generate signal (1 if close > rolling_mean else 0)
Calculate metrics (signal_rate, latency, rows_processed)
Save results to metrics.json
Write logs to run.log
Run Locally

Install dependencies:
pip install -r requirements.txt

Run project:
python run.py --input data.csv --config config.yaml --output metrics.json --log-file run.log

Run with Docker

Build image:
docker build -t mlops-task .

Run container:
docker run --rm mlops-task

Output Example

{
"version": "v1",
"rows_processed": 9996,
"metric": "signal_rate",
"value": 0.49,
"latency_ms": 120,
"seed": 42,
"status": "success"
}

Tech Stack:
Python
Pandas
NumPy
PyYAML
Docker
Logging

Key Learnings:
MLOps pipeline design
Data validation and preprocessing
Reproducibility using seed + config
Docker-based deployment
Observability using logs and metrics
Author

Khushwant Singh Rajat
GitHub: https://github.com/Khushwant123-x

LinkedIn: https://www.linkedin.com/in/khushwant-singh-rajat