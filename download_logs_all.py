import os
import re
import requests
import tarfile
from tqdm import tqdm

DATA_DIR = "data"
CLEAN_FILE = "data/clean_logs_updated.txt"

os.makedirs(DATA_DIR, exist_ok=True)

# Example dataset URLs (Zenodo mirrors)
datasets = {
    "HDFS": "https://zenodo.org/record/3227177/files/HDFS_1.tar.gz",
    "Apache": "https://zenodo.org/record/3227177/files/Apache.tar.gz",
    "Linux": "https://zenodo.org/record/3227177/files/Linux.tar.gz",
    "Spark": "https://zenodo.org/record/3227177/files/Spark.tar.gz"
}


def download_dataset(name, url):
    file_path = os.path.join(DATA_DIR, f"{name}.tar.gz")

    if os.path.exists(file_path):
        print(f"{name} already downloaded")
        return file_path

    print(f"Downloading {name}...")

    response = requests.get(url, stream=True)
    total = int(response.headers.get('content-length', 0))

    with open(file_path, "wb") as f:
        for data in tqdm(response.iter_content(1024), total=total//1024):
            f.write(data)

    return file_path


def extract_dataset(file_path):
    print("Extracting:", file_path)

    with tarfile.open(file_path, "r:gz") as tar:
        tar.extractall(DATA_DIR)


def clean_log(line):

    # remove timestamps
    line = re.sub(r'^\d+\s+\d+\s+\d+\s+', '', line)

    # remove IP addresses
    line = re.sub(r'\d+\.\d+\.\d+\.\d+(:\d+)?', 'IP', line)

    # remove block ids
    line = re.sub(r'blk_-?\d+', 'block', line)

    # remove file paths
    line = re.sub(r'/[\w/.\-]+', 'PATH', line)

    # remove extra spaces
    line = re.sub(r'\s+', ' ', line)

    return line.strip()


# STEP 1 — Download datasets
for name, url in datasets.items():
    path = download_dataset(name, url)
    extract_dataset(path)


# STEP 2 — Read all log files
clean_logs = []

for root, dirs, files in os.walk(DATA_DIR):

    for file in files:

        if file.endswith(".log"):

            file_path = os.path.join(root, file)

            print("Processing:", file_path)

            with open(file_path, errors="ignore") as f:

                for line in f:

                    cleaned = clean_log(line)

                    if len(cleaned) > 10:
                        clean_logs.append(cleaned)


# STEP 3 — Save cleaned logs
with open(CLEAN_FILE, "w") as f:

    for log in clean_logs:
        f.write(log + "\n")


print("Clean logs saved to:", CLEAN_FILE)
print("Total logs:", len(clean_logs))