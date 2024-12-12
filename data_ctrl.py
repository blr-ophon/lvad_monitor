"""
Hold data that will be accessed by the fsm and the gui

Note: the program will received data from all channels independently (for now).
It can only chose which ones it will plot



When the FSM is in transfer state and data packets are received, fsm calls
appendData to put it in the channel.

The user sets the charts in the DisplayGUI. When he press start, a new thread
will start, taking whatever data user wants from channel via dataCtrl and plotting
in the charts he wants
"""
from dataclasses import dataclass
from enum import Enum


@dataclass
class DataChannel():
    """
    Hold channel specification and data
    """
    sample_rate: int
    # TODO: data_size and date being a list of floats
    data: float


class DataCtrl():
    """
    Control of all data channels
    """
    def __init__(self):
        self.channels: dict[int, DataChannel] = {}
        self.data_rdy = False

        # self.read_thread = None
        # self.write_thread = None

        self.save = False
        self.lock = False

    def newChannel(self, ch_id, sample_rate):
        """
        Configure a new channel
        """
        new_channel = DataChannel(sample_rate, 0)

        self.channels[ch_id] = new_channel
        print(f"Channel {ch_id} added.")

    def appendData(self, enum_data):
        """
        Write data from list to the respective channels
        """
        while self.lock:
            # TODO: lock acquire timeout
            pass
        self.lock = True

        for ch_id, ch_data in enum_data:
            self.channels[int(ch_id)].data = ch_data

        if self.save:
            # TODO: write to csv file
            pass

        self.lock = False

    def getData(self, ch_id):
        while self.lock:
            # TODO: lock acquire timeout
            pass
        self.lock = True
        data = self.channels[ch_id].data
        self.lock = False
        return data
