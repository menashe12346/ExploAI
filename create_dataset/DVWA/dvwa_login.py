import requests

def dvwa_login(ip="192.168.56.101", username="admin", password="password"):
    login_url = f"http://{ip}/dvwa/login.php"
    session = requests.Session()

    # קבלת טופס עם Token
    token_resp = session.get(login_url)
    if "user_token" not in token_resp.text:
        raise Exception("לא הצלחנו למשוך user_token מהטופס")

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(token_resp.text, 'html.parser')
    token = soup.find('input', {'name': 'user_token'})['value']

    payload = {
        "username": username,
        "password": password,
        "Login": "Login",
        "user_token": token
    }

    # התחברות
    resp = session.post(login_url, data=payload)
    if "Logout" in resp.text:
        print("[+] התחברות הצליחה ל-DVWA")
        return session
    else:
        raise Exception("[-] התחברות נכשלה ל-DVWA")

# בדיקה ידנית:
if __name__ == "__main__":
    session = dvwa_login()
