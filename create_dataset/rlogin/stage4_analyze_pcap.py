from scapy.all import rdpcap, TCP, IP
import json
import os

# שם קובץ ה-PCAP שתרצי לנתח (עדכני לפי הצורך)
PCAP_FILE = "attack_rlogin_20250325_214837.pcap"

def analyze_pcap(pcap_path):
    if not os.path.exists(pcap_path):
        print(f"[-] קובץ {pcap_path} לא נמצא.")
        return

    packets = rdpcap(pcap_path)
    print(f"[+] נקראו {len(packets)} מנות מהקובץ.")

    analysis = {
        "total_packets": len(packets),
        "protocols_detected": set(),
        "connections": [],
        "timestamps": {
            "first_packet": None,
            "last_packet": None
        }
    }

    for i, pkt in enumerate(packets):
        if IP in pkt and TCP in pkt:
            src_ip = pkt[IP].src
            dst_ip = pkt[IP].dst
            sport = pkt[TCP].sport
            dport = pkt[TCP].dport
            flags = pkt[TCP].flags
            time = pkt.time
            payload = bytes(pkt[TCP].payload)

            analysis["protocols_detected"].add("TCP")

            if analysis["timestamps"]["first_packet"] is None:
                analysis["timestamps"]["first_packet"] = float(time)
            analysis["timestamps"]["last_packet"] = float(time)

            connection = {
                "src": src_ip,
                "dst": dst_ip,
                "sport": sport,
                "dport": dport,
                "flags": str(flags),
                "payload_size": len(payload),
                "payload_preview": payload[:20].hex()
            }

            analysis["connections"].append(connection)

    # הפיכת set לרשימה
    analysis["protocols_detected"] = list(analysis["protocols_detected"])

    # שמירת התוצאה כ-JSON
    json_name = pcap_path.replace(".pcap", ".analysis.json")
    with open(json_name, "w") as f:
        json.dump(analysis, f, indent=2)

    print(f"[+] ניתוח הסתיים. JSON שמור כ: {json_name}")

if __name__ == "__main__":
    analyze_pcap(PCAP_FILE)
