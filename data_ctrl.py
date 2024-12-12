"""
Hold data that will be accessed by the fsm and the gui

Note: the program will received data from all channels independently (for now).
It can only chose which ones it will plot

"""
from dataclasses import dataclass
from enum import Enum


@dataclass
class DataChannel():
    """
    Hold channel specification and data
    """
    ch_id: int
    sample_rate: int
    # TODO: data_size and date being a list of floats
    data: float


class DataCtrl():
    """
    Control of all data channels
    """
    def __init__(self):
        self.channels: dict[int, DataChannel] = {}
        self.data_rdy = False;

        self.read_thread = None;
        self.write_thread = None;

    def newChannel(self, ch_id, sample_rate):
        """
        Configure a new channel
        """
        new_channel = DataChannel(ch_id, sample_rate, None)
        self.channels[ch_id] = new_channel
        # print(f"Channel {ch_id} added.")

    def appendData(self, ch_id, data):
        """
        Add new data to channel
        """
        self.channels[ch_id].data = data
