import os
import json

all_cves = []

# מעבר על כל הקבצים בתיקייה הנוכחית
for filename in sorted(os.listdir(".")):
    if filename.endswith(".json"):
        with open(filename, 'r') as f:
            try:
                data = json.load(f)
                all_cves.extend(data.get("CVE_Items", []))
            except json.JSONDecodeError:
                print(f"שגיאה בקריאת הקובץ: {filename}")

# שמירה לקובץ JSON חדש
output_file = "all_cves_combined.json"
with open(output_file, "w") as f:
    json.dump(all_cves, f, indent=2)

print(f"\nTotal CVEs combined: {len(all_cves)}")
print(f"הקובץ נשמר בשם: {output_file}")
