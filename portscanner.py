import socket
import time
import threading
import argparse

startTime = time.time()

parser = argparse.ArgumentParser("Usage: port_scanner.py -i  Taregt in IP -sp [START_PORT] -ep [END_PORT]")
parser.add_argument("-i", "--target", required=True, help=" IP address")
parser.add_argument("-sp", "--start-port", type=int, help="Start port for scanning")
parser.add_argument("-ep", "--end-port", type=int, help="End port for scanning")
args = parser.parse_args()

target = args.target
start_port = args.start_port or 1
end_port = args.end_port or 1024

print('Starting scan on host:', target)

def scan_port(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        conn = s.connect_ex((target, port))
        if conn == 0:
            print('Port %d: OPEN' % port)
        s.close()
    except Exception as e:
        print(f"Error scanning port {port}: {e}")

threads = []

try:
    for i in range(start_port, end_port + 1):
        thread = threading.Thread(target=scan_port, args=(i,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

except KeyboardInterrupt:
    print("\nScan interrupted by user.")

print('Time taken:', time.time() - startTime)
