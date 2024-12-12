import tkinter as tk
import matplotlib.pyplot as pplt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# fig: pplt.Figure
# canvas: FigureCanvasTkAgg
# plot1: pplt.Axes

class ChartGUI():
    def __init__(self, frame):
        self.frame = frame
        self.fig = None
        self.canvas = None
        self.plot1 = None
        # self.plot_list
        self.channels_list = []

        self.drawGraph()

    def drawGraph(self):
        """
        Add pypplot graph to chart
        """
        self.fig = pplt.Figure(figsize=(7, 5), dpi=80)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.plot1 = self.fig.add_subplot(111)

        self.canvas.get_tk_widget().grid(column=1, row=0, rowspan=17,
                                    columnspan=4, sticky="N")

    def drawChannelMenu(self):
        pass

    def destroy(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.frame.destroy()


class ChartsManagerGUI():
    def __init__(self, root, dataCtrl):
        self.root = root
        self.dataCtrl = dataCtrl

        self.frames = []
        self.framesCol = 0
        self.framesRow = 4
        self.total_charts = 0

        # list of chart data for each chart
        self.Charts = []

    def newChart(self):
        """
        Frame where all charts will be
        """
        self.total_charts +=1

        frame = tk.LabelFrame(
            master=self.root,
            text=f"Display Manager - {len(self.frames)+1}",
            padx=5, pady=5, bg="white"
        )
        self.frames.append(frame)
        frame_index = self.total_charts-1
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

        new_chart = ChartGUI(frame)
        self.Charts.append(new_chart)

        self.adjustRootFrame()
# 
#     def chart_addBtnFrame(self):
#         btnH = 2
#         btnW = 4
# 
#         # Create frame and widgets
#         frame = tk.LabelFrame(
#             master=self.frames[-1],
#             pady=5,
#             bg="white",
#         )
# 
#         btn_addCh = tk.Button(
#             master=frame,
#             text="+", bg="white",
#             width=btnW, height=btnH,
#         )
# 
#         btn_delCh = tk.Button(
#             master=frame,
#             text="-", bg="white",
#             width=btnW, height=btnH
#         )
#         btn_addCh.grid(column=0, row=0, padx=5, pady=5)
# 
#         # Publish frame and widgets
#         frame.grid(column=0, row=0, padx=5, pady=5, sticky="N")
#         btn_addCh.grid(column=0, row=0, padx=5, pady=5, sticky="NW")
#         btn_delCh.grid(column=1, row=0, padx=5, pady=5, sticky="NW")
# 
#         # Append frame and widgets to list and append list
#         frame_list = []
#         frame_list.append(frame)
#         frame_list.append(btn_addCh)
#         frame_list.append(btn_delCh)
#         self.charts_frames.append(frame_list)

    def killChart(self):
        """
        Remove last chart from screen
        """
        if self.total_charts > 0:
            self.total_charts -= 1

            chart = self.Charts.pop()
            chart.destroy()

            self.adjustRootFrame()

    def adjustRootFrame(self):
        """
        Resize window to accomodate chart frames
        """
        rootWidth = 905
        rootHeight = 130 + 430 * (int((self.total_charts-1)/2)+1)

        if self.total_charts > 1:
            rootWidth = 905*2

        if self.total_charts == 0:
            rootHeight = 130

        self.root.geometry(f"{rootWidth}x{rootHeight}")
