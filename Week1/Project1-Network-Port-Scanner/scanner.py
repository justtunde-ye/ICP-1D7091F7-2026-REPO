import socket
from datetime import datetime

print("=" * 50)
print("Advanced Network Port Scanner")
print("=" * 50)

target = input("Enter target IP or hostname: ")

try:
    target_ip = socket.gethostbyname(target)
except socket.gaierror:
    print("Error: Unable to resolve hostname.")
    exit()

start_port = int(input("Enter starting port: "))
end_port = int(input("Enter ending port: "))

print(f"\nScanning target: {target_ip}")
print(f"Time started: {datetime.now()}")
print("-" * 50)

start_time = datetime.now()

try:
    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)

        result = sock.connect_ex((target_ip, port))

        if result == 0:
            try:
                service = socket.getservbyport(port)
            except OSError:
                service = "Unknown"

            print(f"[OPEN] Port {port:<5} Service: {service}")

        sock.close()

except KeyboardInterrupt:
    print("\nScan cancelled by user.")

except Exception as e:
    print(f"\nError: {e}")

finally:
    finish_time = datetime.now()
    print("-" * 50)
    print(f"Scan completed in {finish_time - start_time}")