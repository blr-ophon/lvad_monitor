from gui_master import RootGUI, CommGUI

RootMaster = RootGUI()
ComMaster = CommGUI(RootMaster.root)

RootMaster.root.mainloop()
