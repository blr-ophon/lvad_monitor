from serial.tools import list_ports
import serial


class SerialCtrl():
    """
    Serial port operations
    """
    def __init__(self):
        self.com_list = []
        self.ser = None         # serial.Serial
        self.status = False     # Indicates successful port opening

    def getCOMList(self):
        """
        Update list of available ports
        """
        self.com_list = [port.device for port in list_ports.comports()
                         if self.isValidPort(port)]
        self.com_list.insert(0, "-")

    def SerialOpen(self, port, baudrate):
        """
        Open serial port and establish connection
        """
        try:
            if self.ser and self.ser.is_open:
                print("Port already open.")
                self.status = False
                return
        except AttributeError:
            pass

        try:
            # Instantiating Serial automatically tries to open port
            self.ser = serial.Serial(
                    port=port,
                    baudrate=baudrate,
                    timeout=0.1,
            )
            self.status = True
            print(f"Opened port: {self.ser.port} (baud: {self.ser.baudrate})")
        except Exception as e:
            # Failed opening port
            self.status = False
            print(f"Error opening port: {e}")

    def SerialClose(self):
        """
        Stop serial connection with current port
        """
        try:
            self.ser.close()
            self.status = False
        except Exception as e:
            self.status = False
            print(f"Error closing port: {e}")

    def listen(self):
        """
        Poll for messages
        """
        msg = self.ser.read_until(b"$")
        if msg:
            print(f"      << {msg}")
        return msg if msg else None

    def send(self, msg):
        print(f">> {msg}")
        self.ser.write(msg.encode("utf-8"))

    @staticmethod
    def isValidPort(port):
        """
        Check if a port is an MCU serial port (USB, UART or ACM)
        """
        return "USB" in port.description \
            or "UART" in port.description or "ACM" in port.device


if __name__ == "__main__":
    SerialCtrl()
