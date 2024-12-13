import tkinter as tk
import matplotlib.pyplot as pplt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading

# fig: pplt.Figure
# canvas: FigureCanvasTkAgg
# plot1: pplt.Axes

class ChartGUI():
    """
    Single chart with graph and manageable channels to plot
    """
    def __init__(self, frame, channels):
        self.frame = frame
        self.channels = channels

        self.fig = None
        self.canvas = None
        self.axes = None

        self.checkbox_vars = []

        # Plotting
        self.x_data = []
        self.y_data = []
        self.index = 0

        self.drawGraph()
        self.drawChannelMenu()

    def plot(self):
        # self.axes.set_xlim([min(data), max(data)])
        # self.axes.set_ylim([min(data), max(data)])
        self.start_animation()

        # plotting the graph
        # self.axes.plot(y)
        # self.canvas.draw()

        return
        # data = [channels[1]
        for i in range(len(self.channels)):
            if self.checkbox_vars[i].get():
                # Plot
                self.axes.plot(list(self.channels[i].data))
                # breakpoint()
        self.canvas.draw()

    def drawGraph(self):
        """
        Add pypplot graph to chart
        """
        self.fig = pplt.Figure(figsize=(7, 5), dpi=80)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.axes = self.fig.add_subplot(111)

        self.canvas.get_tk_widget().grid(column=1, row=0, rowspan=17,
                                         columnspan=4, sticky="N")

        ##########
        self.line, = self.axes.plot([], [], 'b-')  # Initialize an empty plot
        self.start_animation()
        ##########

    def start_animation(self):
        if self.index <= 100:
            self.x_data.append(self.index)
            self.y_data.append(self.index**2)

            self.line.set_data(self.x_data, self.y_data)
            self.axes.set_xlim(0, 100)
            self.axes.set_ylim(0, 10000)
            self.canvas.draw()

            self.index += 1

    def drawChannelMenu(self):
        """
        Draw channel menu with checkboxes
        """
        main_frame = tk.LabelFrame(master=self.frame, text="Available Channels", bg="white")
        main_frame.grid(column=0, row=0, padx=5, pady=5, sticky="N")

        for i in range(len(self.channels)):
            sub_frame = tk.Frame(master=main_frame)
            sub_frame.grid(row=i, column=0, pady=5, padx=5, sticky="w")

            var = tk.IntVar()
            self.checkbox_vars.append(var)

            checkbox = tk.Checkbutton(sub_frame, text=f"Channel {i}", variable=var)
            checkbox.grid(row=0, column=0, padx=5)

    def destroy(self):
        """
        Remove chart with all it's widgets
        """
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.frame.destroy()


class ChartsManagerGUI():
    """
    Manages all charts
    """
    def __init__(self, root, dataStream):
        self.root = root
        self.dataCtrl = dataStream

        self.frames = []
        self.framesCol = 0
        self.framesRow = 4
        self.total_charts = 0

        # list of chart data for each chart
        self.Charts = []

        # Threading
        self.plotThread = None
        self.new_data = None

    def initPlotTask(self):
        self.plotThread = threading.Thread(target=self.plotData, daemon=True)
        self.new_data = threading.Condition()
        self.plotThread.start()

    def plotData(self):
        """
        Start plotting all charts
        """
        while True:
            with self.new_data:
                if self.total_charts > 0:
                    for chart in self.Charts:
                        chart.plot()
                self.new_data.wait()

    def triggerPlot(self):
        with self.new_data:
            self.new_data.notify()

    def newChart(self):
        """
        Frame where all charts will be
        """
        self.total_charts += 1

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

        new_chart = ChartGUI(frame, self.dataCtrl.channels)
        self.Charts.append(new_chart)

        self.adjustRootFrame()

    def destroy(self):
        for chart in self.Charts:
            self.total_charts -= 1

            chart.destroy()

            self.adjustRootFrame()

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
