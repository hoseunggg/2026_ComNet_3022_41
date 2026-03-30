"""
UDP Server
"""
import os
import time
from socket import *

serverName = "10.10.10.2"
serverPort = 5000

chunk_size = 512
expected_bytes = 3 * 1024 * 1024

processing_delay = 0.0
recv_buffer_size = 65536
timeout_seconds = 2.0

expected_chunks = (expected_bytes + chunk_size - 1) // chunk_size
output_file = "received_udp_sample.txt"

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind((serverName, serverPort))
serverSocket.settimeout(timeout_seconds)

print("[UDP SERVER] Ready")

received_map = {}
received_chunks = 0
total_received = 0
clientAddress = None

start_time = None

serverSocket.settimeout(None)

while True:
    try:
        packet, addr = serverSocket.recvfrom(recv_buffer_size)
    except timeout:
        print("[UDP SERVER] Time break")
        break

    if clientAddress is None:
        clientAddress = addr
        start_time = time.time()
        serverSocket.settimeout(timeout_seconds)
        print(f"[UDP SERVER] Transfer started from {clientAddress}")

    header, payload = packet.split(b" ", 1)
    seq = int(header.decode()[3:]) 

    recv_time = time.time()
    if seq not in received_map:
        last_data_time = recv_time
        received_map[seq] = payload
        received_chunks += 1
        total_received += len(payload)

        print(f"[UDP SERVER] Received DATA seq={seq} payload={len(payload)} bytes | "
              f"total_chunks={received_chunks}/{expected_chunks}")

    if processing_delay > 0:
        time.sleep(processing_delay)


with open(output_file, "wb") as f:
    for seq in range(1, expected_chunks + 1):
        if seq in received_map:
            f.write(received_map[seq])

end_time = time.time()
transfer_time = recv_time - start_time if start_time else 0
throughput = total_received / transfer_time if transfer_time > 0 else 0

missing_seqs = [seq for seq in range(1, expected_chunks + 1) if seq not in received_map]
missing_count = len(missing_seqs)

is_incomplete = missing_count > 0
status = "INCOMPLETE" if is_incomplete else "OK"

with open(output_file, "rb") as f:
    total_lines = sum(1 for _ in f)

print("[UDP SERVER] Transfer finished")
print(f"[UDP SERVER] Received chunks: {received_chunks}/{expected_chunks}")
print(f"[UDP SERVER] Missing chunks: {missing_count}")
print(f"[UDP SERVER] Incomplete: {is_incomplete}")
print(f"[UDP SERVER] Transfer time: {transfer_time:.6f} s")
print(f"[UDP SERVER] File saved: {output_file}")
print(f"[UDP SERVER] Total bytes: {total_received}/{expected_bytes}")
print(f"[UDP SERVER] Total lines: {total_lines}")
print(f"[UDP SERVER] Throughput: {throughput:.2f} bytes/s")

result = (
    f"RESULT : {status}, Total received bytes : {total_received}, Transfer time : {transfer_time:.6f}, Throughput : {throughput:.2f} bytes/s"
)


os.remove(output_file)

serverSocket.sendto(result.encode(), clientAddress)
print(f"[UDP SERVER] Sent result: {result}")

serverSocket.close()
print("[UDP SERVER] Closed")







