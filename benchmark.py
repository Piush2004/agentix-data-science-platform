import requests
import time
import pandas as pd
import numpy as np
import psutil
import os
import json

BASE_URL = "http://localhost:8000/api/v1"

def generate_dataset(size_mb, filename):
    # Rough estimate: 1 row of 10 floats is ~80 bytes.
    # 1MB = 1,000,000 bytes -> 12,500 rows.
    rows = int((size_mb * 1024 * 1024) / 80)
    df = pd.DataFrame({
        f'col_{i}': np.random.rand(rows) for i in range(9)
    })
    df['target'] = np.random.randint(0, 2, size=rows)
    df.to_csv(filename, index=False)
    return rows, 10, os.path.getsize(filename)

def get_process_metrics():
    process = psutil.Process()
    mem = process.memory_info().rss / (1024 * 1024)
    cpu = process.cpu_percent(interval=0.1)
    return mem, cpu

def run_benchmark():
    datasets = [
        {"size_mb": 1, "name": "bench_1mb.csv"},
        {"size_mb": 5, "name": "bench_5mb.csv"},
        {"size_mb": 20, "name": "bench_20mb.csv"}
    ]
    
    results = []
    
    for ds in datasets:
        print(f"Generating {ds['name']}...")
        rows, cols, size_bytes = generate_dataset(ds["size_mb"], ds["name"])
        
        metrics = {
            "dataset": ds["name"],
            "rows": rows,
            "cols": cols,
            "size_mb": size_bytes / (1024 * 1024),
            "upload_time": 0,
            "profile_time": 0,
            "fe_time": 0,
            "automl_time": 0,
            "xai_time": 0,
            "peak_mem": 0,
            "peak_cpu": 0
        }
        
        # 1. Upload
        start = time.time()
        mem_start, cpu_start = get_process_metrics()
        with open(ds["name"], "rb") as f:
            res = requests.post(f"{BASE_URL}/dataset/upload", files={"file": (ds["name"], f, "text/csv")})
        metrics["upload_time"] = time.time() - start
        
        mem_curr, cpu_curr = get_process_metrics()
        metrics["peak_mem"] = max(metrics["peak_mem"], mem_curr)
        metrics["peak_cpu"] = max(metrics["peak_cpu"], cpu_curr)
        
        # 2. Profile
        start = time.time()
        res = requests.post(f"{BASE_URL}/platform/profile", json={"dataset_name": ds["name"]})
        metrics["profile_time"] = time.time() - start
        
        # 3. Feature Engineering
        start = time.time()
        res = requests.post(f"{BASE_URL}/platform/feature-engineering", json={"dataset_name": ds["name"]})
        metrics["fe_time"] = time.time() - start
        
        # 4. AutoML
        start = time.time()
        res = requests.post(f"{BASE_URL}/platform/predict", json={"dataset_name": ds["name"], "target_column": "target"})
        metrics["automl_time"] = time.time() - start
        
        # 5. XAI
        start = time.time()
        res = requests.get(f"{BASE_URL}/platform/xai?dataset_name={ds['name']}")
        metrics["xai_time"] = time.time() - start
        
        results.append(metrics)
        print(f"Completed {ds['name']}")
        
    with open('benchmark_results.json', 'w') as f:
        json.dump(results, f, indent=4)
        
if __name__ == "__main__":
    run_benchmark()
