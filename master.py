from gui_master import RootGUI, CommGUI
from serial_com_ctrl import SerialCtrl


MySerial = SerialCtrl()

RootMaster = RootGUI()

ComMaster = CommGUI(RootMaster.root, MySerial)

RootMaster.root.mainloop()
