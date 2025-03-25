import subprocess
import datetime

# כתובת IP של הקורבן ידועה מראש
VICTIM_IP = "192.168.56.101"
INTERFACE = "vboxnet0"  # שנה לפי הצורך אם את משתמשת בממשק אחר

def get_timestamp():
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

def start_capture():
    filename = f"monitor_rlogin_{get_timestamp()}.pcap"
    print(f"[+] Starting tcpdump on interface '{INTERFACE}'")
    print(f"[+] Saving to: {filename}")

    cmd = [
        "sudo", "tcpdump",
        "-i", INTERFACE,
        f"host {VICTIM_IP}",
        "-w", filename
    ]

    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n[+] Capture stopped by user.")
    except Exception as e:
        print("[-] Error:", e)

if __name__ == "__main__":
    start_capture()
