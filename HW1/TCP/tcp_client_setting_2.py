"""
TCP Client
"""
import os
import time
from socket import *

serverName = "10.10.10.2"
serverPort = 5000

chunk_size = 256
send_delay = 0.0

file_name = "sample.txt"
file_size = 3 * 1024 * 1024

if os.path.exists(file_name):
    os.remove(file_name)
if not os.path.exists(file_name):
    with open(file_name, "w", encoding="utf-8") as f:
        line_no = 1
        while f.tell() + chunk_size <= file_size:
            line = f"{line_no:010d} "
            remain = chunk_size - len(line) - 1

            if remain < 0:
                line = line[:chunk_size - 1]
                remain = 0

            f.write(line + "A" * remain + "\n")
            line_no += 1

total_bytes = os.path.getsize(file_name)
total_chunks = (total_bytes + chunk_size - 1) // chunk_size

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.settimeout(25.0)
clientSocket.connect((serverName, serverPort))

sent_bytes = 0
seq = 0

start_time = time.time()
next_send_time = time.time()

with open(file_name, "rb") as f:
    while True:
        chunk = f.read(chunk_size)
        if not chunk:
            break

        now = time.time()
        if now < next_send_time:
            time.sleep(next_send_time - now)

        seq += 1
        clientSocket.sendall(chunk)
        sent_bytes += len(chunk)

        print(f"[TCP CLIENT] Sent DATA seq={seq} payload={len(chunk)} bytes | "
              f"total_bytes={sent_bytes}/{total_bytes}")

        next_send_time += send_delay
        # time.sleep(send_delay)
end_time = time.time()
send_phase_time = end_time - start_time
print(f"[TCP CLIENT] Send phase time: {send_phase_time:.6f} s")

clientSocket.shutdown(SHUT_WR)

result_data = b""
while True:
    chunk = clientSocket.recv(4096)
    if not chunk: break
    result_data += chunk

result_text = result_data.decode().strip()
print(f"[TCP CLIENT] Received result: {result_text}")

setting_name = "SETTING 2"
protocol_name = "TCP"
prefix = f"{setting_name} {protocol_name} = "
new_line = prefix + str(result_text)

with open("result_tcp_setting_2.txt", "w", encoding="utf-8") as f:
    f.write(new_line + "\n")

os.remove(file_name)
clientSocket.close()