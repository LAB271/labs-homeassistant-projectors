import socket
import logging

DOMAIN = "vivitek_projector"

def setup(hass, config):
    conf = config[DOMAIN]
    host = conf.get("host")
    port = conf.get("port", 7000)
    projector = VivitekProjector(host, port)

    hass.data[DOMAIN] = projector
    return True

class VivitekProjector:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def send_command(self, command):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.host, self.port))
                s.sendall((command + '\r').encode())
                response = s.recv(1024)
                return response.decode().strip()
        except Exception as e:
            logging.error(f"Error sending command: {e}")
            return None

    def power_on(self):
        return self.send_command("op power.on")

    def power_off(self):
        return self.send_command("op power.off")

    def status(self):
        return self.send_command("op status ?")
