import tkinter as tk
import matplotlib.pyplot as pplt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from dataclasses import dataclass
from functools import partial


@dataclass
class ChartData():
    """
    Hold pyplot objects for chart
    """
    fig: pplt.Figure
    canvas: FigureCanvasTkAgg
    plot1: pplt.Axes
"""
    chart root frame
    chart index
"""


class ChartsGUI():
    def __init__(self, root, dataCtrl):
        self.root = root
        self.dataCtrl = dataCtrl

        self.frames = []
        self.framesCol = 0
        self.framesRow = 4
        self.totalframes = 0

        # list of chart data for each chart
        self.charts_data = []
        # list of lists of control frames for each chart
        self.charts_frames = []

        self.ChannelMenu = []
        self.ViewVar = []
        self.OptionVar = []
        self.FunVar = []

    def newChart(self):
        """
        Append new chart to the screen
        """
        self.totalframes+=1
        # Create chart frame
        self.chart_addMasterFrame()
        # Menus
        self.chart_addChannelMenu()
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
        """
        Add pypplot graph to chart
        """
        fig = pplt.Figure(figsize=(7, 5), dpi=80)
        canvas = FigureCanvasTkAgg(fig, master=self.frames[-1])
        plot1 = fig.add_subplot(111)

        chart_data = ChartData(fig, canvas, plot1)

        canvas.get_tk_widget().grid(column=1, row=0, rowspan=17,
                                    columnspan=4, sticky="N")

        self.charts_data.append(chart_data)

    def chart_addBtnFrame(self):
        btnH = 2
        btnW = 4

        # Create frame and widgets
        frame = tk.LabelFrame(
            master=self.frames[-1],
            pady=5,
            bg="white",
        )

        btn_addCh = tk.Button(
            master=frame,
            text="+", bg="white",
            width=btnW, height=btnH,
            command=partial(self.addChannel, self.ChannelMenu[-1])
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
        self.charts_frames.append(frame_list)

###############################################################################
    # def chart_addChannelFrame(self):
    def chart_addChannelMenu(self):
        """
        Methods that adds the main frame that will manage the frames of the options
        """

        # New lists for current chart
        self.ChannelMenu.append([])
        self.ViewVar.append([])
        self.OptionVar.append([])
        self.FunVar.append([])

        # Create base frame for menus
        ch_tk_frame = tk.LabelFrame(self.frames[-1], pady=5, bg="white")
        self.ChannelMenu[-1].append(ch_tk_frame)
        self.ChannelMenu[-1].append(self.totalframes)
        ch_tk_frame.grid( column=0, row=1, padx=5, pady=5, rowspan=16, sticky="N")
        # OK!

        self.addChannel(self.ChannelMenu[-1])

    def addChannel(self, channel_menu):
        '''
        Method that initiate the channel frame which will provide options & control to the user
        '''
        ch_menu_frame = channel_menu[0]     # tk LabelFrame
        chart_index = channel_menu[1]-1       # chart index

        if len(ch_menu_frame.winfo_children()) < 8:
            # Labelframe to hold checkbutton
            NewFrameChannel = tk.LabelFrame(ch_menu_frame, bg="white")
            NewFrameChannel.grid(column=0,
                                 row=len(ch_menu_frame.winfo_children())-1)

            # Checkbutton 
            # self.ViewVar[-1].append(tk.IntVar())
            holdvar = tk.IntVar()
            Ch_btn = tk.Checkbutton(
                master=NewFrameChannel,
                # variable=self.ViewVar[chart_index][len(self.ViewVar[chart_index])-1],
                variable=holdvar,
                onvalue=1, offvalue=0, bg="white"
            )
            self.ViewVar[chart_index].append(holdvar)

            Ch_btn.grid(row=0, column=0, padx=1)
# OK!
            # Option menu
            # self.ChannelOption(NewFrameChannel, chart_index)
            # self.ChannelFunc(NewFrameChannel, chart_index)

    def ChannelOption(self, Frame, chart_index):
        holdvar = tk.StringVar()
        # self.OptionVar[chart_index].append(tk.StringVar())

        bds = self.dataCtrl.Channels

        self.OptionVar[chart_index][len(
            self.OptionVar[chart_index])-1].set(bds[0])
        drop_ch = tk.OptionMenu(Frame, self.OptionVar[chart_index][len(
            self.OptionVar[chart_index])-1], *bds)
        
        drop_ch.config(width=5)
        drop_ch.grid(row=0, column=1, padx=1)

        self.OptionVar[chart_index].append(holdvar)

    def ChannelFunc(self, Frame, ChannelFrameNumber):
        pass

###############################################################################
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

            self.charts_frames.pop()
            self.charts_data.pop()

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
