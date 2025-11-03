import os
import json
# from ip_address import get_local_ip
import socket

def get_local_ip():
    global ip
    
    try:
        # Connect to a public server (Google DNS, for example)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # We never actually send data
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        pass


class ConfigureVariables:
    """
   setting variables
   
    """
 
    def __init__(self):
        self.config = {}
        

    def set_IP(self):
        self.config['IPaddress'] = get_local_ip()
        
    def get_config_path(self):
        base = os.path.expanduser("~/.config")
        return os.path.join(base, "sim_racing_dash.json")
 
    def load_config(self):
        path = self.get_config_path()
        if os.path.exists(path):
            with open(path, "r") as f:
                self.config = json.load(f)
                self.set_IP()
        
        # If the files doesnt exist already
        self.set_IP()
 
    def save_config(self, config):
        path = self.get_config_path()
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump(config, f)
            


 


c = ConfigureVariables()

c.load_config()

print(c.config)