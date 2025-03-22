import pandas as pd
import re

# File paths
CVE_CSV_PATH = "/home/menashe/cyber_ai_project/datasets/processed/cve_dataset_cleaned.csv"
EXPLOIT_CSV_PATH = "/home/menashe/cyber_ai_project/datasets/processed/exploitdb_dataset.csv"
CLEAN_CVE_CSV_PATH = "/home/menashe/cyber_ai_project/datasets/processed/cve_dataset_cleaned.csv"
CLEAN_EXPLOIT_CSV_PATH = "/home/menashe/cyber_ai_project/datasets/processed/exploitdb_dataset_cleaned.csv"

# Function to clean text fields
def clean_text(text):
    if pd.isna(text) or text.strip() == "":
        return "Unknown"
    text = re.sub(r"\s+", " ", text)  # Remove extra spaces
    text = re.sub(r"[^\x00-\x7F]+", "", text)  # Remove non-ASCII characters
    return text.strip()

# Function to clean the CVE dataset
def clean_cve_dataset():
    print("🔹 Cleaning CVE dataset...")

    # Read CSV with error handling
    df_cve = pd.read_csv(CVE_CSV_PATH, encoding="utf-8", on_bad_lines="skip", dtype=str)

    # Drop empty rows
    df_cve.dropna(subset=["CVE ID", "Description"], inplace=True)

    # Clean text fields
    df_cve["CVE ID"] = df_cve["CVE ID"].apply(clean_text)
    df_cve["Description"] = df_cve["Description"].apply(clean_text)
    df_cve["Severity"] = df_cve["Severity"].apply(clean_text)
    
    # Check if 'Affected Products' exists before cleaning
    if "Affected Products" in df_cve.columns:
        df_cve["Affected Products"] = df_cve["Affected Products"].apply(clean_text)
    else:
        df_cve["Affected Products"] = "Unknown"

    # Save cleaned dataset
    df_cve.to_csv(CLEAN_CVE_CSV_PATH, index=False, encoding="utf-8")
    print(f"✅ CVE dataset cleaned and saved to {CLEAN_CVE_CSV_PATH}")

# Function to clean the ExploitDB dataset
def clean_exploit_dataset():
    print("🔹 Cleaning ExploitDB dataset...")

    # Read CSV with error handling
    df_exploit = pd.read_csv(EXPLOIT_CSV_PATH, encoding="utf-8", on_bad_lines="skip", dtype=str)

    # Print column names for debugging
    print("📌 ExploitDB dataset columns:", df_exploit.columns.tolist())

    # Clean text fields if columns exist
    if "Exploit Name" in df_exploit.columns:
        df_exploit["Exploit Name"] = df_exploit["Exploit Name"].apply(clean_text)
    if "Exploit Code" in df_exploit.columns:
        df_exploit["Exploit Code"] = df_exploit["Exploit Code"].apply(clean_text)

    # Fix column naming for exploit path
    path_column = None
    for col in df_exploit.columns:
        if "path" in col.lower():
            path_column = col
            break

    if path_column:
        df_exploit[path_column] = df_exploit[path_column].apply(clean_text)
    else:
        print("⚠️ No 'Exploit Path' column found. Skipping path cleaning.")

    # Save cleaned dataset
    df_exploit.to_csv(CLEAN_EXPLOIT_CSV_PATH, index=False, encoding="utf-8")
    print(f"✅ ExploitDB dataset cleaned and saved to {CLEAN_EXPLOIT_CSV_PATH}")

# Run cleaning functions
clean_cve_dataset()
clean_exploit_dataset()
print("🎯 All datasets cleaned successfully!")
