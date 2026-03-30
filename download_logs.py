import os
import requests
from tqdm import tqdm
import tarfile

DATA_DIR = "data"
URL = "https://zenodo.org/record/3227177/files/HDFS_1.tar.gz"

os.makedirs(DATA_DIR, exist_ok=True)

file_path = os.path.join(DATA_DIR, "hdfs_logs.tar.gz")

print("Downloading dataset...")

response = requests.get(URL, stream=True)
total_size = int(response.headers.get('content-length', 0))

with open(file_path, 'wb') as f:
    for data in tqdm(response.iter_content(1024), total=total_size//1024):
        f.write(data)

print("Download complete.")