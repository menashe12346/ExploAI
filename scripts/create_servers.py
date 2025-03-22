import pandas as pd
import re

# נתיב לקובץ ה-exploit
CSV_PATH = "/home/menashe/cyber_ai_project/datasets/exploits/exploitdb/exploit_v1.csv"
OUTPUT_PATH = "/home/menashe/cyber_ai_project/datasets/exploits/exploitdb/servers.csv"

# טען את הקובץ
print("📥 טוען את הקובץ:", CSV_PATH)
df = pd.read_csv(CSV_PATH)

# הכנה
servers = []
seen = set()
server_id = 1

# עיבוד כל שורת אקפלויט
total = len(df)
for idx, row in df.iterrows():
    affected = str(row.get("affected_products", ""))
    if not affected or affected.strip() == "":
        continue

    cpes = [c.strip() for c in affected.split(";") if c.strip().startswith("cpe:2.3:")]
    os_list = []
    services = []

    for cpe in cpes:
        parts = cpe.split(":")
        if len(parts) < 6:
            continue
        cpe_type = parts[2]
        vendor = parts[3]
        product = parts[4]
        version = parts[5]

        # מערכת הפעלה
        if cpe_type == "o":
            os_id = f"{vendor}:{product}:{version}"
            os_list.append({
                "vendor": vendor,
                "name": product,
                "version": version,
                "cpe": cpe,
                "os_id": os_id
            })

        # שירותים/אפליקציות
        elif cpe_type == "a":
            services.append(f"{product} {version}".strip())

    # שייך שירותים לכל מערכת הפעלה בקבוצה
    for os_data in os_list:
        os_id = os_data["os_id"]
        if os_id in seen:
            continue
        seen.add(os_id)
        servers.append({
            "server_id": server_id,
            "os_vendor": os_data["vendor"],
            "os_name": os_data["name"],
            "os_version": os_data["version"],
            "services": "; ".join(services) if services else "",
            "cpe_raw": os_data["cpe"]
        })
        print(f"🖥️  [{server_id}] נוספה מערכת: {os_data['vendor']} {os_data['name']} {os_data['version']} עם {len(services)} שירותים")
        server_id += 1

print(f"\n✅ הסתיים. נמצאו {len(servers)} שרתים ייחודיים מתוך {total} אקפלויטים.")

# שמור לקובץ
servers_df = pd.DataFrame(servers)
servers_df.to_csv(OUTPUT_PATH, index=False)
print(f"💾 הקובץ נשמר בהצלחה: {OUTPUT_PATH}")
