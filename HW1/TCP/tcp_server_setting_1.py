"""
TCP Server
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


output_file = "received_tcp_sample.txt"

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((serverName, serverPort))
serverSocket.listen(1)

print("[TCP SERVER] Ready")


connectionSocket, clientAddress = serverSocket.accept()

print(f"[TCP SERVER] Transfer started from {clientAddress}")

total_received = 0
start_time = time.time()

with open(output_file, "wb") as f:
    while True:
        data = connectionSocket.recv(recv_buffer_size)
        if not data: break

        f.write(data)
        total_received += len(data)

        print(f"[TCP SERVER] Received {len(data)} bytes | total_bytes={total_received}")

        if processing_delay > 0:
            time.sleep(processing_delay)

end_time = time.time()
transfer_time = end_time - start_time if start_time > 0 else 0
throughput = total_received / transfer_time if transfer_time > 0 else 0

with open(output_file, "rb") as f:
    total_lines = sum(1 for _ in f)

print("[TCP SERVER] Transfer finished")
print(f"[TCP SERVER] File saved: {output_file}")
print(f"[TCP SERVER] Total bytes: {total_received}/{expected_bytes}")
print(f"[TCP SERVER] Total lines: {total_lines}")
print(f"[TCP SERVER] Throughput: {throughput:.2f} bytes/s")


result = (
    f"RESULT : Complete, Total received bytes : {total_received}, Transfer time : {transfer_time:.6f}, Throughput : {throughput:.2f} bytes/s"
)

os.remove(output_file)

connectionSocket.sendall(result.encode())
print(f"[TCP SERVER] Sent result: {result}")

connectionSocket.close()
print("[TCP SERVER] Ready")