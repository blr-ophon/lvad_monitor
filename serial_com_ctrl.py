from serial.tools import list_ports
import serial


class SerialCtrl():
    """
    Serial port operations
    """
    def __init__(self):
        self.com_list = []
        self.ser = None         # Serial.Serial
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
            # Instantiating automatically tries to open port
            self.ser = serial.Serial(
                    port=port,
                    baudrate=baudrate,
                    timeout=0.1,
            )
            self.status = True
            print(f"Opened port: {self.ser.port}")

        except Exception as e:
            # Failed opening port
            self.status = False
            print(f"Failed to open port: {e}")

    def SerialClose(self):
        """
        Stop serial connection with current port
        """
        try:
            self.ser.close()
            self.status = False
        except:
            self.status = False

    @staticmethod
    def isValidPort(port):
        """
        Check if a port is an MCU serial port (USB, UART or ACM)
        """
        return "USB" in port.description \
            or "UART" in port.description or "ACM" in port.device


if __name__ == "__main__":
    SerialCtrl()