import tkinter as tk

class RootGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Serial Communication")
        self.root.geometry("360x120")
        self.root.config(bg="white")


class CommGUI():
    """Communication Manager menu"""
    def __init__(self, root):
        self.root = root
        # Create Frame
        self.frame = tk.LabelFrame(master=root, text="Communication", padx=5,
                                   pady=5, bg="white")
        # Create Label inside frame
        self.label_com = tk.Label(self.frame, text="Available Port(s): ",
                                  bg="white", width=15, anchor="w")
        self.label_bd = tk.Label(self.frame, text="Baud rate: ",
                                 bg="white", width=15, anchor="w")
        self.ComOptionMenu()
        self.BaudOptionMenu()

        # Create 'Refresh' and 'Connect' buttons
        self.btn_refresh = tk.Button(master=self.frame, text="Refresh",
                                     width=10, command=self.com_refresh)
        self.btn_connect = tk.Button(master=self.frame, text="Connect",
                                     width=10, state="disabled",
                                     command=self.com_connect)

        self.padx = 20
        self.pady = 5
        self.publish()

    def ComOptionMenu(self):
        """Create a drop menu widget to select Comm port"""
        coms = ["-", "COM3"]
        # StringVar is needed to operate with OptionMenu widget
        self.clicked_com = tk.StringVar()
        self.clicked_com.set(coms[0])
        self.drop_com = tk.OptionMenu(
                self.frame,     # master
                self.clicked_com,
                *coms,
                command=self.connect_ctrl,
        )
        self.drop_com.config(width=10)

    def BaudOptionMenu(self):
        """Create a drop menu widget to select Baud Rate"""
        bds = ["-",
               "300",
               "600",
               "1200",
               "2400",
               "4800",
               "9600",
               "14400",
               "19200",
               "28800",
               "38400",
               "56000",
               "57600",
               "115200",
               "128000",
               "256000",]
        self.clicked_bd = tk.StringVar()
        self.clicked_bd.set(bds[0])
        self.drop_bd = tk.OptionMenu(
                self.frame,
                self.clicked_bd,
                *bds,
                command=self.connect_ctrl,
        )
        self.drop_bd.config(width=10)

    def connect_ctrl(self, arg):
        """
        Enable 'Connect' button when a value from the 2 drop menus is selected
        """
        if "-" in (self.clicked_com.get(), self.clicked_bd.get()):
            self.btn_connect["state"] = "disable"
        else:
            self.btn_connect["state"] = "active"

    def com_refresh(self):
        print("refresh")

    def com_connect(self):
        print("connect")

    def publish(self):
        """Publish widgets grid on Communication frame"""
        # Root
        self.frame.grid(row=0, column=0, rowspan=3,
                        columnspan=3, padx=5, pady=5)

        # Communication
        self.label_com.grid(column=1, row=2)
        self.drop_com.grid(column=2, row=2)
        self.drop_bd.grid(column=2, row=3)
        self.label_bd.grid(column=1, row=3)
        self.btn_refresh.grid(column=3, row=2)
        self.btn_connect.grid(column=3, row=3)


if __name__ == "__main__":
    RootGUI()
    CommGUI()
