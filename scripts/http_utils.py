"""Shared HTTP + retrieval-logging utilities for ESPN structured-data acquisition."""
import csv
import json
import os
import time
from datetime import datetime, timezone

import requests

RAW_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "raw_espn")
LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "retrieval_log.csv")

LOG_COLUMNS = [
    "retrieved_at",
    "request_url",
    "season",
    "season_type",
    "week",
    "http_status",
    "raw_event_count",
    "parsed_event_count",
    "retry_count",
    "notes",
]


def ensure_log_header():
    if not os.path.exists(LOG_PATH):
        with open(LOG_PATH, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=LOG_COLUMNS)
            writer.writeheader()


def append_log_row(row: dict):
    ensure_log_header()
    with open(LOG_PATH, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=LOG_COLUMNS)
        writer.writerow({k: row.get(k, "") for k in LOG_COLUMNS})


def fetch_json(url, season="", season_type="", week="", max_retries=3, timeout=30, notes=""):
    """GET url, save raw response verbatim, log the attempt, return (status, parsed_json_or_None, raw_text)."""
    retry_count = 0
    last_status = None
    last_text = None
    while retry_count <= max_retries:
        try:
            resp = requests.get(url, timeout=timeout)
            last_status = resp.status_code
            last_text = resp.text
            if resp.status_code == 200:
                try:
                    parsed = resp.json()
                except ValueError:
                    parsed = None
                    notes = (notes + "; " if notes else "") + "JSON decode error on 200 response"
                return resp.status_code, parsed, resp.text, retry_count, notes
            else:
                notes = (notes + "; " if notes else "") + f"HTTP {resp.status_code} on attempt {retry_count + 1}"
        except requests.RequestException as e:
            notes = (notes + "; " if notes else "") + f"Request exception on attempt {retry_count + 1}: {e}"
        retry_count += 1
        if retry_count <= max_retries:
            time.sleep(2 ** retry_count)
    return last_status, None, last_text, retry_count - 1, notes


def save_raw(subdir, filename, raw_text):
    d = os.path.join(RAW_DIR, subdir)
    os.makedirs(d, exist_ok=True)
    path = os.path.join(d, filename)
    with open(path, "w") as f:
        f.write(raw_text if raw_text is not None else "")
    return path


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
