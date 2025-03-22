import pandas as pd
import csv

# נתיבים לקובצי הנתונים
CVE_CSV_PATH = "/home/menashe/cyber_ai_project/datasets/processed/cve_dataset.csv"
FIXED_CVE_CSV_PATH = "/home/menashe/cyber_ai_project/datasets/processed/cve_dataset_fixed.csv"

def fix_cve_csv():
    print("🔹 מתקן את קובץ CVE...")

    with open(CVE_CSV_PATH, "r", encoding="utf-8", errors="replace") as infile, \
         open(FIXED_CVE_CSV_PATH, "w", encoding="utf-8", newline="") as outfile:

        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # קריאה וכתיבת הכותרת
        header = next(reader, None)
        if not header:
            print("❌ שגיאה: לא נמצאה כותרת בקובץ CVE.")
            return
        writer.writerow(header)

        # רשימה לשמירת הנתונים התקינים
        cleaned_rows = []
        last_row = None  # שמירת שורה קודמת לתיקון שורות קטועות

        for row in reader:
            if len(row) < len(header):  # אם השורה קטועה
                if last_row:
                    last_row[-1] += " " + " ".join(row)  # חיבור לשדה האחרון בשורה הקודמת
                continue
            
            cleaned_rows.append(row)
            last_row = row  # עדכון השורה האחרונה התקינה

        # כתיבת השורות הנקיות לקובץ
        writer.writerows(cleaned_rows)

    print(f"✅ קובץ CVE תוקן ונשמר ב- {FIXED_CVE_CSV_PATH}")

# הפעלת התיקון
fix_cve_csv()
