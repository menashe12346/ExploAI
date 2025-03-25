import subprocess
import datetime
import time

VICTIM_IP = "192.168.56.101"
INTERFACE = "vboxnet0"
CAPTURE_DURATION = 20  # כמה שניות להקליט אחרי זיהוי

def get_timestamp():
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

def detect_and_capture():
    # הפקודה שמאזינה לפעילות rlogin
    monitor_cmd = [
        "sudo", "tcpdump",
        "-l",
        "-n",
        "-i", INTERFACE,
        f"tcp and port 513 and host {VICTIM_IP}"
    ]

    print(f"[*] מאזין ל־rlogin בממשק {INTERFACE} מול {VICTIM_IP}")
    with subprocess.Popen(monitor_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True) as monitor_proc:
        try:
            for line in monitor_proc.stdout:
                print(f"[!] זוהתה פעילות rlogin: {line.strip()}")
                
                # עצירת ההאזנה ברגע שזוהה
                monitor_proc.terminate()
                monitor_proc.wait()

                # הפעלת הקלטת tcpdump
                timestamp = get_timestamp()
                pcap_filename = f"attack_rlogin_{timestamp}.pcap"
                print(f"[+] מתחיל הקלטת pcap ל־{CAPTURE_DURATION} שניות → {pcap_filename}")

                capture_cmd = [
                    "sudo", "timeout", str(CAPTURE_DURATION),
                    "tcpdump",
                    "-i", INTERFACE,
                    f"host {VICTIM_IP} and port 513",
                    "-w", pcap_filename
                ]

                subprocess.run(capture_cmd)
                print(f"[+] הסתיימה ההקלטה. קובץ שמור בשם: {pcap_filename}")
                break  # עוצר אחרי מתקפה אחת
        except KeyboardInterrupt:
            print("\n[+] עצירה ידנית")

if __name__ == "__main__":
    detect_and_capture()
