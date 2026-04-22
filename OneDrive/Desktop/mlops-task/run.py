import argparse
import pandas as pd
import numpy as np
import yaml
import json
import logging
import time
import sys
import os

def setup_logging(log_file):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

def load_config(config_path):
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        required = ["seed", "window", "version"]
        for key in required:
            if key not in config:
                raise ValueError(f"Missing config key: {key}")

        return config
    except Exception as e:
        raise ValueError(f"Config error: {str(e)}")

def load_data(input_path):
    if not os.path.exists(input_path):
        raise FileNotFoundError("Input file not found")

    try:
        df = pd.read_csv(input_path)

        # 🔥 FIX (IMPORTANT)
        df.columns = df.columns.str.strip().str.lower()

    except Exception:
        raise ValueError("Invalid CSV format")

    if df.empty:
        raise ValueError("Empty dataset")

    if "close" not in df.columns:
        raise ValueError("Missing 'close' column")

    return df

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--log-file", required=True)

    args = parser.parse_args()

    setup_logging(args.log_file)
    logging.info("Job started")

    start_time = time.time()

    try:
        # Load config
        config = load_config(args.config)
        seed = config["seed"]
        window = config["window"]
        version = config["version"]

        np.random.seed(seed)
        logging.info(f"Config loaded: {config}")

        # Load data
        df = load_data(args.input)
        logging.info(f"Rows loaded: {len(df)}")

        # Rolling mean
        logging.info("Calculating rolling mean")
        df["rolling_mean"] = df["close"].rolling(window=window).mean()

        # Signal
        logging.info("Generating signal")
        df = df.dropna()
        df["signal"] = (df["close"] > df["rolling_mean"]).astype(int)

        rows_processed = len(df)
        signal_rate = df["signal"].mean()

        latency_ms = int((time.time() - start_time) * 1000)

        metrics = {
            "version": version,
            "rows_processed": rows_processed,
            "metric": "signal_rate",
            "value": round(float(signal_rate), 4),
            "latency_ms": latency_ms,
            "seed": seed,
            "status": "success"
        }

        logging.info(f"Metrics: {metrics}")

        with open(args.output, "w") as f:
            json.dump(metrics, f, indent=2)

        print(json.dumps(metrics, indent=2))

        logging.info("Job completed successfully")
        sys.exit(0)

    except Exception as e:
        latency_ms = int((time.time() - start_time) * 1000)

        error_output = {
            "version": "v1",
            "status": "error",
            "error_message": str(e)
        }

        logging.error(str(e))

        with open(args.output, "w") as f:
            json.dump(error_output, f, indent=2)

        print(json.dumps(error_output, indent=2))

        sys.exit(1)

if __name__ == "__main__":
    main()