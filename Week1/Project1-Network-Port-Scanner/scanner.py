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
open_ports = []
report_file = "scan_results.txt"

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

            open_ports.append((port, service))
            print(f"[OPEN] Port {port:<5} Service: {service}")

        sock.close()

except KeyboardInterrupt:
    print("\nScan cancelled by user.")

except Exception as e:
    print(f"\nError: {e}")

finally:
    finish_time = datetime.now()

    with open(report_file, "w") as report:
        report.write("Advanced Network Port Scanner Report\n")
        report.write("=" * 40 + "\n")
        report.write(f"Target Host : {target}\n")
        report.write(f"Target IP   : {target_ip}\n")
        report.write(f"Scan Date   : {datetime.now()}\n\n")

        report.write("Open Ports\n")
        report.write("-" * 40 + "\n")

        for port, service in open_ports:
            report.write(f"{port:<6} {service}\n")

        report.write("\n")
        report.write(f"Ports Scanned : {end_port - start_port + 1}\n")
        report.write(f"Open Ports    : {len(open_ports)}\n")
        report.write(f"Scan Duration : {finish_time - start_time}\n")

    print("-" * 50)
    print("SCAN SUMMARY")
    print("-" * 50)

    print(f"Target Host  : {target}")
    print(f"Target IP    : {target_ip}")
    print(f"Ports Scanned: {end_port - start_port + 1}")
    print(f"Open Ports   : {len(open_ports)}")

    if open_ports:
        print("\nOpen Port List")
        print("-" * 50)

        for port, service in open_ports:
            print(f"{port:<6} {service}")

    print("-" * 50)
    print(f"Scan completed in {finish_time - start_time}")

    print("-" * 50)
    print("SCAN SUMMARY")
    print("-" * 50)

    print(f"Target Host  : {target}")
    print(f"Target IP    : {target_ip}")
    print(f"Ports Scanned: {end_port - start_port + 1}")
    print(f"Open Ports   : {len(open_ports)}")

    if open_ports:
        print("\nOpen Port List")
        print("-" * 50)

        for port, service in open_ports:
            print(f"{port:<6} {service}")

    print("-" * 50)
    print(f"Scan completed in {finish_time - start_time}")