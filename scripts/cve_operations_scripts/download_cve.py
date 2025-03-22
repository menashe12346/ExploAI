import os
import requests
from tqdm import tqdm
import gzip
import shutil

# הגדרת הנתיב לתיקיית ההורדה
download_dir = os.path.expanduser("~/cve_data")
os.makedirs(download_dir, exist_ok=True)

# רשימת השנים להורדה
years = list(range(2002, 2025))
base_url = "https://nvd.nist.gov/feeds/json/cve/1.1"

# פונקציית הורדה עם פס התקדמות
def download_file(url, dest_path):
    response = requests.get(url, stream=True)
    total = int(response.headers.get('content-length', 0))
    with open(dest_path, 'wb') as file, tqdm(
        desc=os.path.basename(dest_path),
        total=total,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(chunk_size=1024):
            file.write(data)
            bar.update(len(data))

# הורדת קבצים לפי שנה
for year in years:
    filename = f"nvdcve-1.1-{year}.json.gz"
    url = f"{base_url}/{filename}"
    dest_path = os.path.join(download_dir, filename)
    download_file(url, dest_path)

# הורדת קבצי recent ו-modified
for name in ["recent", "modified"]:
    filename = f"nvdcve-1.1-{name}.json.gz"
    url = f"{base_url}/{filename}"
    dest_path = os.path.join(download_dir, filename)
    download_file(url, dest_path)

# חילוץ כל קבצי gz
for file in os.listdir(download_dir):
    if file.endswith(".gz"):
        gz_path = os.path.join(download_dir, file)
        json_path = gz_path[:-3]
        with gzip.open(gz_path, 'rb') as f_in:
            with open(json_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        os.remove(gz_path)  # מחיקת קובץ ה-gz לאחר חילוץ

print("ההורדה והחילוץ הסתיימו בהצלחה.")
import os
import requests
from tqdm import tqdm
import gzip
import shutil

# הגדרת הנתיב לתיקיית ההורדה
download_dir = os.path.expanduser("~/cve_data")
os.makedirs(download_dir, exist_ok=True)

# רשימת השנים להורדה
years = list(range(2002, 2025))
base_url = "https://nvd.nist.gov/feeds/json/cve/1.1"

# פונקציית הורדה עם פס התקדמות
def download_file(url, dest_path):
    response = requests.get(url, stream=True)
    total = int(response.headers.get('content-length', 0))
    with open(dest_path, 'wb') as file, tqdm(
        desc=os.path.basename(dest_path),
        total=total,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(chunk_size=1024):
            file.write(data)
            bar.update(len(data))

# הורדת קבצים לפי שנה
for year in years:
    filename = f"nvdcve-1.1-{year}.json.gz"
    url = f"{base_url}/{filename}"
    dest_path = os.path.join(download_dir, filename)
    download_file(url, dest_path)

# הורדת קבצי recent ו-modified
for name in ["recent", "modified"]:
    filename = f"nvdcve-1.1-{name}.json.gz"
    url = f"{base_url}/{filename}"
    dest_path = os.path.join(download_dir, filename)
    download_file(url, dest_path)

# חילוץ כל קבצי gz
for file in os.listdir(download_dir):
    if file.endswith(".gz"):
        gz_path = os.path.join(download_dir, file)
        json_path = gz_path[:-3]
        with gzip.open(gz_path, 'rb') as f_in:
            with open(json_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        os.remove(gz_path)  # מחיקת קובץ ה-gz לאחר חילוץ

print("ההורדה והחילוץ הסתיימו בהצלחה.")
