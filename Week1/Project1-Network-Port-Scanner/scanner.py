import socket
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor


def banner():
    print("=" * 50)
    print("Advanced Network Port Scanner")
    print("=" * 50)


def scan_port(target_ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)

    result = sock.connect_ex((target_ip, port))
    sock.close()

    if result == 0:
        try:
            service = socket.getservbyport(port)
        except OSError:
            service = "Unknown"
        return (port, service)

    return None


def save_report(filename, target, target_ip, start_port, end_port,
                open_ports, start_time, finish_time):

    with open(filename, "w") as report:
        report.write("Advanced Network Port Scanner Report\n")
        report.write("=" * 40 + "\n")
        report.write(f"Target Host : {target}\n")
        report.write(f"Target IP   : {target_ip}\n")
        report.write(f"Scan Date   : {datetime.now()}\n\n")

        report.write("Open Ports\n")
        report.write("-" * 40 + "\n")

        for port, service in sorted(open_ports):
            report.write(f"{port:<6} {service}\n")

        report.write("\n")
        report.write(f"Ports Scanned : {end_port - start_port + 1}\n")
        report.write(f"Open Ports    : {len(open_ports)}\n")
        report.write(f"Scan Duration : {finish_time - start_time}\n")


def main():

    banner()

    target = input("Enter target IP or hostname: ")

    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        print("Unable to resolve hostname.")
        return

    start_port = int(input("Enter starting port: "))
    end_port = int(input("Enter ending port: "))

    print(f"\nScanning target: {target_ip}")
    print(f"Time started: {datetime.now()}")
    print("-" * 50)

    start_time = datetime.now()
    open_ports = []

    with ThreadPoolExecutor(max_workers=100) as executor:

        futures = [
            executor.submit(scan_port, target_ip, port)
            for port in range(start_port, end_port + 1)
        ]

        for future in futures:
            result = future.result()

            if result:
                open_ports.append(result)
                print(f"[OPEN] Port {result[0]:<5} Service: {result[1]}")

    finish_time = datetime.now()

    save_report(
        "scan_results.txt",
        target,
        target_ip,
        start_port,
        end_port,
        open_ports,
        start_time,
        finish_time
    )

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

        for port, service in sorted(open_ports):
            print(f"{port:<6} {service}")

    print("-" * 50)
    print(f"Scan completed in {finish_time - start_time}")


if __name__ == "__main__":
    main()