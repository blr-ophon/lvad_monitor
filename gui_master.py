import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import matplotlib.pyplot as pplt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from serial_fsm import SerialFSM, FSMState

# TODO: geometry variables in separated file

class RootGUI():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("LVAD Monitor")
        self.root.geometry("385x130")
        self.root.config(bg="white")


class CommGUI():
    # TODO: Organize this class. Put all attributes in __init__. Rename some functions
    """Communication Manager menu"""
    def __init__(self, root, serialCtrl, dataCtrl):
        self.root = root
        self.serialCtrl = serialCtrl
        self.dataCtrl = dataCtrl
        self.conn = None
        self.serial_fsm = SerialFSM(serialCtrl, dataCtrl, self)

        # FRAME
        self.frame = tk.LabelFrame(master=root, text="Communication", padx=5,
                                   pady=5, bg="white")
        # WIDGETS
        self.lbl_com = tk.Label(self.frame, text="Available Port(s): ",
                                bg="white", width=15, anchor="w")
        self.lbl_bd = tk.Label(self.frame, text="Baud rate: ",
                               bg="white", width=15, anchor="w")

        # Create 'Refresh' and 'Connect' buttons
        self.btn_refresh = tk.Button(master=self.frame, text="Refresh",
                                     width=10, command=self.com_refresh)
        self.btn_connect = tk.Button(master=self.frame, text="Connect",
                                     width=10, state="disabled",
                                     command=self.serial_connect)

        self.ComOptionMenu()
        self.BaudOptionMenu()

        self.padx = 20
        self.pady = 5
        self.publish()

    def ComOptionMenu(self):
        """
        Create a drop menu widget to select Comm port
        """

        # Scan COM ports
        self.serialCtrl.getCOMList()
        coms = self.serialCtrl.com_list

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
        bds = ["-", "300", "600", "1200", "2400", "4800",
               "9600", "14400", "19200", "28800", "38400",
               "56000", "57600", "115200", "128000", "256000"]

        self.clicked_bd = tk.StringVar()
        self.clicked_bd.set(bds[0])
        self.drop_bd = tk.OptionMenu(
                self.frame,
                self.clicked_bd,
                *bds,
                command=self.connect_ctrl,
        )
        self.drop_bd.config(width=10)

    def connect_ctrl(self, widget):
        """
        Enable 'Connect' button when a value from the 2 drop menus is selected
        """
        if "-" in (self.clicked_com.get(), self.clicked_bd.get()):
            self.btn_connect["state"] = "disable"
        else:
            self.btn_connect["state"] = "active"

    def com_refresh(self):
        """
        Rescan serial ports to display on drop menu
        """
        self.drop_com.destroy()
        self.ComOptionMenu()
        self.drop_com.grid(column=2, row=2)
        self.connect_ctrl(None)

    def serial_connect(self):
        # TODO: change 'connect' to 'open port' to avoid confusion with fsm connect state
        """
        Executed when 'Connect' button is pressed. Try to establish serial
        connection
        """
        if self.btn_connect["text"] in "Connect":
            # Try connecting
            PORT = self.clicked_com.get()
            BAUD = self.clicked_bd.get()
            self.serialCtrl.SerialOpen(port=PORT, baudrate=BAUD)

            if self.serialCtrl.status:
                # Connection was successful
                self.btn_connect["text"] = "Disconnect"
                self.btn_refresh["state"] = "disable"
                self.drop_bd["state"] = "disable"
                self.drop_com["state"] = "disable"
                # InfoMsg = f"port {self.serialCtrl.ser.port} \
                #             successfully opened"
                # messagebox.showinfo("showinfo", InfoMsg)

                # Create connection manager and start serial fsm thread
                self.conn = ConnGUI(self.root, self.serial_fsm, self.dataCtrl)

                self.serial_fsm.start()
                self.serial_fsm.set_state(FSMState.SYNC)

            else:
                ErrorMsg = f"Failure to establish serial connection using\
                            {self.clicked_com.get()}"
                messagebox.showerror("showerror", ErrorMsg)
        else:
            self.serial_disconnect()

    def serial_disconnect(self):
        """
        Close the connection
        """
        self.serial_fsm.stop()          # Close fsm
        self.serialCtrl.SerialClose()   # Close port
        self.conn.ConnGUIClose()        # Close menu

        self.btn_connect["text"] = "Connect"
        self.btn_refresh["state"] = "active"
        self.drop_bd["state"] = "active"
        self.drop_com["state"] = "active"

    def publish(self):
        """Publish widgets grid on Communication frame"""
        # Root
        self.frame.grid(row=0, column=0, rowspan=3,
                        columnspan=3, padx=5, pady=5)
        # Communication
        self.lbl_com.grid(column=1, row=2)
        self.drop_com.grid(column=2, row=2)
        self.drop_bd.grid(column=2, row=3)
        self.lbl_bd.grid(column=1, row=3)
        self.btn_refresh.grid(column=3, row=2)
        self.btn_connect.grid(column=3, row=3)


class ConnGUI():
    """
    Connection manager menu
    """
    def __init__(self, root, serial_fsm, dataCtrl):
        self.root = root
        self.serial_fsm = serial_fsm
        self.dataCtrl = dataCtrl

        self.active_channels = None

        self.padx = 20
        self.pady = 15

        # FRAME
        self.frame = tk.LabelFrame(
                master=root,
                text="Connection Manager",
                padx=5,
                pady=5,
                bg="white",
                width=60
        )

        # WIDGETS
        self.lbl_sync = tk.Label(
                master=self.frame,
                text="Sync Status: ",
                bg="white",
                width=15,
                anchor="w"
        )
        self.lbl_sync_status = tk.Label(
                master=self.frame,
                text="...Sync...",
                bg="white",
                fg="orange",
                width=5,
        )
        self.lbl_ch = tk.Label(
                master=self.frame,
                text="Active channels: ",
                bg="white",
                width=15,
                anchor="w"
        )
        self.lbl_ch_status = tk.Label(
                master=self.frame,
                text="...",
                bg="white",
                fg="orange",
                width=5,
        )
        self.btn_start_stream = tk.Button(
            master=self.frame,
            text="Start",
            state="disabled",
            width=5,
            command=self.start_stream
        )

        self.btn_stop_stream = tk.Button(
            master=self.frame,
            text="Stop",
            state="disabled",
            width=5,
            command=self.stop_stream
        )
        self.btn_add_chart = tk.Button(
                master=self.frame,
                text="+",
                state="disabled",
                width=5,
                bg="white",
                fg="#098577",
                command=self.add_chart
        )

        self.btn_kill_chart = tk.Button(
                master=self.frame,
                text="-",
                state="disabled",
                width=5,
                bg="white",
                fg="#CC252C",
                command=self.kill_chart
        )

        self.save = False
        self.SaveVar = tk.IntVar()
        self.chkbtn_save = tk.Checkbutton(
                master=self.frame, text="Save data", variable=self.SaveVar,
                onvalue=1, offvalue=0, bg="white", state="disabled",
                command=self.save_data)

        # Additional

        self.separator = ttk.Separator(self.frame, orient="vertical")

        # Publish
        self.ConnGUIOpen()
        self.dis = DisplayGUI(self.root, self.dataCtrl)

    def ConnGUIOpen(self):
        """
        Publish menu on the window
        """
        self.root.geometry("905x130")
        self.frame.grid(row=0, column=4, rowspan=3, columnspan=5,
                        padx=5, pady=5)

        self.lbl_sync.grid(column=1, row=1)
        self.lbl_sync_status.grid(column=2, row=1)

        self.lbl_ch.grid(column=1, row=2)
        self.lbl_ch_status.grid(column=2, row=2, pady=self.pady)

        self.btn_start_stream.grid(column=3, row=1, padx=self.padx)
        self.btn_stop_stream.grid(column=3, row=2, padx=self.padx)

        self.btn_add_chart.grid(column=4, row=1, padx=self.padx)
        self.btn_kill_chart.grid(column=5, row=1, padx=self.padx)

        self.chkbtn_save.grid(column=4, row=2, columnspan=2)

        self.separator.place(relx=0.56, rely=0, relwidth=0.001, relheight=1)

    def ConnGUIClose(self):
        """
        Close connection manager menu
        """
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.frame.destroy()
        self.root.geometry("385x130")

    def status_connected(self, channels_n):
        # TODO: remove function argument, let it take channel number from
        # dataCtrl
        self.active_channels = channels_n

        self.lbl_sync_status["text"] = "OK"
        self.lbl_sync_status["fg"] = "green"

        self.lbl_ch_status["text"] = str(self.active_channels)
        self.lbl_ch_status["fg"] = "green"

        self.btn_start_stream["state"] = "active"
        self.btn_stop_stream["state"] = "active"
        if channels_n > 0:
            self.btn_add_chart["state"] = "active"
            self.btn_kill_chart["state"] = "active"
            self.chkbtn_save["state"] = "active"

    def status_syncing(self):
        self.lbl_sync_status["text"] = "Syncing..."
        self.lbl_sync_status["fg"] = "orange"

        self.lbl_ch_status["text"] = "..."
        self.lbl_ch_status["fg"] = "orange"

        self.btn_start_stream["state"] = "disabled"
        self.btn_stop_stream["state"] = "disabled"
        self.btn_add_chart["state"] = "disabled"
        self.btn_kill_chart["state"] = "disabled"
        self.chkbtn_save["state"] = "disabled"

    def status_failed(self):
        self.lbl_sync_status["text"] = "Failed"
        self.lbl_sync_status["fg"] = "red"

        self.lbl_ch_status["text"] = "..."
        self.lbl_ch_status["fg"] = "red"

        self.btn_start_stream["state"] = "disabled"
        self.btn_stop_stream["state"] = "disabled"
        self.btn_add_chart["state"] = "disabled"
        self.btn_kill_chart["state"] = "disabled"
        self.chkbtn_save["state"] = "disabled"

    def start_stream(self):
        """
        Request data from MCU according to user specification
        and plot them in the specified charts
        """
        # TODO: get input from button
        self.serial_fsm.request_data(1)

    def stop_stream(self):
        self.serial_fsm.stop_request()

    def add_chart(self):
        self.dis.newChart()

    def kill_chart(self):
        self.dis.killChart()

    def save_data(self):
        pass



class DisplayGUI():
    def __init__(self, root, dataCtrl):
        self.root = root
        self.dataCtrl = dataCtrl

        self.frames = []
        self.framesCol = 0
        self.framesRow = 4
        self.totalframes = 0

        # list of lists of figures for each chart
        self.figures = []
        # list of lists of control frames for each chart
        self.controlFrames = []

    def newChart(self):
        """
        Append new chart to the screen
        """
        self.totalframes+=1
        # Create chart frame
        self.chart_addMasterFrame()
        # Normal widgets
        self.chart_addBtnFrame()
        # Create graph
        self.chart_addGraph()

        self.adjustRootFrame()


    def chart_addMasterFrame(self):
        """
        Frame where all charts will be
        """

        frame = tk.LabelFrame(
            master=self.root,
            text=f"Display Manager - {len(self.frames)+1}",
            padx=5, pady=5, bg="white"
        )
        self.frames.append(frame)
        frame_index = self.totalframes-1
        # tmp_totalframes = len(self.frames)-1

        if frame_index % 2 == 0:
            self.framesCol = 0
        else:
            self.framesCol = 9
        self.framesRow = 4 + (4 * int(frame_index/2))

        frame.grid(
            padx=5,
            column=self.framesCol,
            row=self.framesRow,
            columnspan=9,
            sticky="NW"
        )

    def chart_addGraph(self):
        # Create figures
        frame_index = self.totalframes-1

        fig = pplt.Figure(figsize=(7, 5), dpi=80)

        plot1 = fig.add_subplot(111)

        canvas = FigureCanvasTkAgg(fig,
                                 master=self.frames[frame_index])

        canvas.get_tk_widget().grid(column=1, row=0, columnspan=17, sticky="N")

        # Append figures to list and append list
        figure_list = []
        figure_list.append(fig)
        figure_list.append(plot1)
        figure_list.append(canvas)
        self.figures.append(figure_list)

    def chart_addBtnFrame(self):
        btnH = 2
        btnW = 4

        frame_index = self.totalframes-1

        # Create frame and widgets
        frame = tk.LabelFrame(
            master=self.frames[frame_index],
            pady=5,
            bg="white",
        )

        btn_addCh = tk.Button(
            master=frame,
            text="+", bg="white",
            width=btnW, height=btnH
        )

        btn_delCh = tk.Button(
            master=frame,
            text="-", bg="white",
            width=btnW, height=btnH
        )
        btn_addCh.grid(column=0, row=0, padx=5, pady=5)

        # Publish frame and widgets
        frame.grid(column=0, row=0, padx=5, pady=5, sticky="N")
        btn_addCh.grid(column=0, row=0, padx=5, pady=5, sticky="NW")
        btn_delCh.grid(column=1, row=0, padx=5, pady=5, sticky="NW")

        # Append frame and widgets to list and append list
        frame_list = []
        frame_list.append(frame)
        frame_list.append(btn_addCh)
        frame_list.append(btn_delCh)
        self.controlFrames.append(frame_list)

    def killChart(self):
        """
        Remove last chart from screen
        """
        if self.totalframes > 0:
            self.totalframes -= 1

            chart_frame = self.frames.pop()
            for widget in chart_frame.winfo_children():
                widget.destroy()
            chart_frame.destroy()

            self.controlFrames.pop()
            self.figures.pop()

            self.adjustRootFrame()

    def adjustRootFrame(self):
        """
        Resize window to accomodate chart frames
        """
        rootWidth = 905
        rootHeight = 130 + 430 * (int((self.totalframes-1)/2)+1)

        if self.totalframes > 1:
            rootWidth = 905*2

        if self.totalframes == 0:
            rootHeight = 130

        self.root.geometry(f"{rootWidth}x{rootHeight}")
        print(f"{rootWidth}x{rootHeight}")



if __name__ == "__main__":
    RootGUI()
    # CommGUI()
    # ConnGUI()
