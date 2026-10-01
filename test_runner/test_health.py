import requests
import psycopg2
import socket
import time
import sys
from datetime import datetime

report_lines = []
test_failed = False

def add_result(test_name, status, message):
    global test_failed

    line = f"{test_name}: {status} - {message}"
    print(line)
    report_lines.append(line)

    if status == "FAIL":
        test_failed = True

def check_web():
    try:
        response = requests.get("http://web:80", timeout=5)
        if response.status_code == 200:
            add_result("Web Server Check", "PASS", "Nginx is reachable")
        else:
            add_result("Web Server Check", "FAIL", f"Status code: {response.status_code}")
    except Exception as e:
        add_result("Web Server Check", "FAIL", str(e))

def check_database():
    for attempt in range(10):
        try:
            conn = psycopg2.connect(
                host="db",
                port=5432,
                database="testdb",
                user="testuser",
                password="testpass"
            )
            conn.close()
            add_result("Database Check", "PASS", "PostgreSQL is reachable")
            return
        except Exception as e:
            print(f"Attempt {attempt + 1}: PostgreSQL not ready yet...")
            time.sleep(3)

    add_result("Database Check", "FAIL", "PostgreSQL did not become reachable after retries")

def check_port(host, port):
    for attempt in range(10):
        try:
            sock = socket.create_connection((host, port), timeout=5)
            sock.close()
            add_result(f"Port Check {host}:{port}", "PASS", "Port is open")
            return
        except Exception:
            print(f"Attempt {attempt + 1}: Port {host}:{port} not open yet...")
            time.sleep(2)

    add_result(f"Port Check {host}:{port}", "FAIL", "Port did not open after retries")

def generate_report():
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_path = f"/app/reports/test_report_{now}.txt"

    with open(report_path, "w") as file:
        file.write("Automated Docker Test Lab Report\n")
        file.write("=" * 40 + "\n\n")
        for line in report_lines:
            file.write(line + "\n")

    print(f"\nReport generated: {report_path}")

if __name__ == "__main__":
    check_web()
    check_database()
    check_port("web", 80)
    check_port("db", 5432)
    generate_report()

    if test_failed:
        print("\nOne or more tests failed.")
        sys.exit(1)

    print("\nAll tests passed.")
    sys.exit(0)