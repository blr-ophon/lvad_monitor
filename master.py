from gui_master import RootGUI, CommGUI
from serial_com_ctrl import SerialCtrl
from data_ctrl import DataCtrl

MySerial = SerialCtrl()
MyData = DataCtrl()

RootMaster = RootGUI()

ComMaster = CommGUI(RootMaster.root, MySerial, MyData)

RootMaster.root.mainloop()
