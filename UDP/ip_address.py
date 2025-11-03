import socket

def get_local_ip():
    try:
        # Connect to a public server (Google DNS, for example)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # We never actually send data
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "Unable to determine IP"

print("🌐 Local IP Address:", get_local_ip())
