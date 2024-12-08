"""
Finite state machine for serial communication

The machine runs on it's on thread and never stops.
It interacts with the whole GUI (connection manager and graphs)
by calling GUI functions made for that purpose, such as:
    Stop Listening
    Disconnect
which handle all GUI related routines
"""

from enum import Enum
from msg_parser import MsgParser

class FSMState(Enum):
    IDLE = 1
    SYNC = 1
    CONNECTED = 1
    LISTENING = 1

class SerialFSM():
    """
    Finite state machine for serial connection
    """
    def __init__(self, serialCtrl, gui):
        self.state = FSMState.IDLE
        self.serial = serialCtrl
        self.parser = MsgParser()

    def start(self):
        """
        Start finite state machine
        """
        # TODO: start thread with run function
        pass

    def stop(self):
        """
        Stop finite state machine
        """
        # TODO: stop thread
        pass

    def run(self):
        while True:
            if self.state == FSMState.IDLE:
                # Do nothing. Wait for user/GUI to change this state to SYNC
                pass
            if self.state == FSMState.SYNC:
                # 1 - Send sync packet
                # 2 - Poll for response
                # 3 - Validate response
                #       Switch to connected
                #       or return to IDLE
                # 4 - Update GUI
                pass
            if self.state == FSMState.CONNECTED:
                # 1 - Update connGUI
                # 2 - Do nothing. Wait for user prompt on GUI
                self.waiting_user = True
                while self.waiting_user:
                    pass
                # 3 - Send message to MCU
                # 4 - Switch state to listening

            if self.state == FSMState.LISTENING:
                # Receive packets periodically
                # Parse data and call GUI to plot it
                # In case of dropped connection, call GUI routine to stop plotting
                # and display error message
                # return to SYNC state
                pass
