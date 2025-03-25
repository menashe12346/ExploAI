import subprocess

# הגדרת הקורבן והממשק
VICTIM_IP = "192.168.56.101"
INTERFACE = "vboxnet0"

# הפקודה שנריץ: tcpdump
CMD = [
    "sudo", "tcpdump",
    "-l",                        # מציג פלט בלייב (live output)
    "-n",                        # לא מנסה לפתור כתובות DNS (מהיר יותר)
    "-i", INTERFACE,            # הממשק להאזנה (vboxnet0)
    f"tcp and port 513 and host {VICTIM_IP}"
]

print("[*] מאזין ל־rlogin... חכה לפעילות 🕵️")

# הפעלת הפקודה וקבלת פלט שורה־שורה
with subprocess.Popen(CMD, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True) as proc:
    try:
        for line in proc.stdout:
            print(f"[!] התגלתה פעילות rlogin:\n{line.strip()}")
    except KeyboardInterrupt:
        print("\n[+] עצרנו האזנה ידנית")
