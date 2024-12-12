import tkinter as tk
import matplotlib.pyplot as pplt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from dataclasses import dataclass


@dataclass
class ChartData():
    """
    Hold pyplot objects for chart
    """
    fig: pplt.Figure
    canvas: FigureCanvasTkAgg
    plot1: pplt.Axes


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
        """
        Add pypplot graph to chart
        """
        fig = pplt.Figure(figsize=(7, 5), dpi=80)
        canvas = FigureCanvasTkAgg(fig, master=self.frames[-1])
        plot1 = fig.add_subplot(111)

        chart_data = ChartData(fig, canvas, plot1)

        canvas.get_tk_widget().grid(column=1, row=0, rowspan=17, 
                                    columnspan=4, sticky="N")

        # Append figures to list and append list
        # figure_list = []
        # figure_list.append(fig)
        # figure_list.append(plot1)
        # figure_list.append(canvas)
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
        self.charts_frames.append(frame_list)

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
        print(f"{rootWidth}x{rootHeight}")
