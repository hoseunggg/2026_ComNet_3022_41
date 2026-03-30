"""
UDP Client
"""
import os
import time
from socket import *

serverName = "10.10.10.2"
serverPort = 5000

chunk_size = 512
send_delay = 0.005

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
                line = line[:chunk_size-1]
                remain = 0

            f.write(line + "A" * remain + "\n")
            line_no += 1

total_bytes = os.path.getsize(file_name)
total_chunks = (total_bytes + chunk_size - 1) // chunk_size

clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(25.0)

sent_bytes = 0
seq = 0

start_time = time.time()
next_send_time = time.time()

with open(file_name, "rb") as f:
    while True:
        chunk = f.read(chunk_size)
        if not chunk: break

        now = time.time()
        if now < next_send_time:
            time.sleep(next_send_time - now)

        seq += 1
        packet = f"SEQ{seq} ".encode() + chunk
        clientSocket.sendto(packet, (serverName, serverPort))

        sent_bytes += len(chunk)

        print(f"[UDP CLIENT] Sent DATA seq={seq} payload={len(chunk)} bytes | "
              f"total_bytes={sent_bytes}/{total_bytes} | "
              f"total_chunks={seq}/{total_chunks}")

        next_send_time += send_delay

end_time = time.time()
send_phase_time = end_time - start_time

print(f"[UDP CLIENT] Send phase time: {send_phase_time:.6f} s")
data, addr = clientSocket.recvfrom(4096)
result_text = data.decode()

print(f"[UDP CLIENT] Received result from {addr}: {result_text}")

setting_name = "SETTING 1"
protocol_name = "UDP"
prefix = f"{setting_name} {protocol_name} = "
new_line = prefix + str(result_text)

with open("result_udp_setting_1.txt", "w", encoding="utf-8") as f:
    f.write(new_line + "\n")

os.remove(file_name)