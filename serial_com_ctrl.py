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
            print(f"Opened port: {self.ser.port}")
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

    def SerialSync(self, gui):
        """
        Synchronize with microcontroller
        """
        # Send initial messages to establish connection and
        # update attributes based on received info (number of channels)
        self.threading = True
        while self.threading:
            try:
                self.ser.write(gui.dataCtrl.sync.encode())
                gui.conn.lbl_sync_status["text"] = "..Sync.."
                gui.conn.lbl_sync_status["fg"] = "orange"
                gui.dataCtrl.RowMsg = self.ser.readline()
            except:
                pass


    def listen(self):
        # Read chunks of data from serial port
        pass

    def parseMsg(self):
        #
        pass

    @staticmethod
    def isValidPort(port):
        """
        Check if a port is an MCU serial port (USB, UART or ACM)
        """
        return "USB" in port.description \
            or "UART" in port.description or "ACM" in port.device


if __name__ == "__main__":
    SerialCtrl()
