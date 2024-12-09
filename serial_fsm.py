"""
Finite state machine for serial communication

The machine runs on it's on thread and never stops.
It interacts with the whole GUI (connection manager and graphs)
by calling GUI functions made for that purpose, such as:
    Stop Listening
    Disconnect
which handle all GUI related routines
"""

import time
import threading
from enum import Enum
from msg_parser import MsgParser, MsgCommand


class FSMState(Enum):
    IDLE = 1
    SYNC = 2
    CONNECTED = 3
    LISTENING = 4


class SerialFSM():
    """
    Finite state machine for serial connection
    """
    def __init__(self, serialCtrl, gui):
        self.state = FSMState.IDLE
        self.serialCtrl = serialCtrl
        self.parser = MsgParser()

        self.running = False
        self.thread = None
        self.condition = threading.Condition()

    def start(self):
        """
        Start finite state machine
        """
        self.running = True
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def stop(self):
        """
        Stop finite state machine
        """
        self.running = False
        self.set_state(FSMState.IDLE)
        self.thread.join()

    def notify(self):
        """
        Notify FSM to wakeup thread when it is waiting for the user input
        or for the gui to change the state
        """
        self.condition.notify()

    def set_state(self, new_state):
        """
        Change FSM state
        """
        with self.condition:
            self.state = new_state
            # Wake up the thread waiting on this condition
            self.condition.notify()

    def run(self):
        """
        FSM loop
        """
        while self.running:
            with self.condition:

                if self.state == FSMState.IDLE:
                    # Do nothing. Wait for user/GUI to change this state
                    print("(FSM) IDLE, waiting for state change")
                    self.condition.wait()

                elif self.state == FSMState.SYNC:
                    print("(FSM) SYNC, waiting for state change")
                    # 1 - Send sync packet
                    self.serialCtrl.send("#?#$")
                    # 2 - Poll for response
                    response = self.serialCtrl.listen()
                    if response is None:
                        pass
                    else:
                        # 3 - Validate response
                        parsed_msg = self.parser.parse(response)
                        if parsed_msg.command == MsgCommand.SYNC_RESP:
                            # Switch to connected
                            self.set_state(FSMState.CONNECTED)
                            #  Update GUI
                        else:
                            # Return to IDLE
                            pass

                elif self.state == FSMState.CONNECTED:
                    # 1 - Update connGUI
                    # 2 - Do nothing. Wait for user prompt on GUI
                    print("(FSM) CONNECTED, waiting for state change")
                    self.condition.wait()
                    # 3 - Send message to MCU
                    # 4 - Switch state to listening

                elif self.state == FSMState.LISTENING:
                    # Receive packets periodically
                    # Parse data and call GUI to plot it
                    # In case of dropped connection, call GUI routine to stop plotting
                    # and display error message
                    # return to SYNC state
                    pass


if __name__ == "__main__":
    fsm = SerialFSM(None, None)
    fsm.start()

    while True:
        fsm.set_state(FSMState.SYNC)
        time.sleep(5)
