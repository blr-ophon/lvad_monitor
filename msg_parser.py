# Future:
# Parse MSFP messages

class MsgParser():
    def __init__(self):
        self.sync = "#?#$"
        self.sync_ok = "!"
        self.StartStream = "#A#$"
        self.StopStream = "#S#$"
        self.SyncChannel = 0
