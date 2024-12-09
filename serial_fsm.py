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

        self.thread = None
        self.condition = threading.Condition()

        self.running = False
        self.parsed_msg = None

        self.gui = gui

    def start(self):
        """
        Start finite state machine
        """
        self.running = True
        self.thread = threading.Thread(target=self.run, daemon=True)
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

    def request_data(self, channels_n):
        """
        send REQUEST message with user specified number of channels
        """
        with self.condition:
            if self.state != FSMState.CONNECTED:
                print("Error: Not connected")
                return
            print(f"Requesting {channels_n} channels")
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

                    # Send sync packet
                    self.serialCtrl.send("#?#$")

                    # Poll for response
                    response = self.serialCtrl.listen()
                    time.sleep(0.5)

                    # Always check if fsm has not been stopped during blocking
                    # operation after it is done
                    # if not self.running:
                    #   continue

                    # Parse and validate response
                    if response is not None:
                        self.parsed_msg = self.parser.parse(response)
                        if self.parsed_msg.command == MsgCommand.SYNC_RESP:
                            # Switch to connected
                            self.set_state(FSMState.CONNECTED)

                        else:
                            # Return to IDLE
                            print("(FSM) SYNC failed")
                            self.set_state(FSMState.IDLE)

                elif self.state == FSMState.CONNECTED:
                    print("(FSM) CONNECTED, waiting for user")

                    #  Update GUI
                    self.gui.conn.connect_successful(self.parsed_msg.channels_n)

                    # TODO: keep connection alive through PING
                    # Do nothing. Wait for user prompt on GUI (Start Button)
                    self.condition.wait()

                    # Send message to MCU
                    # Switch state to listening

                elif self.state == FSMState.LISTENING:
                    print("(FSM) LISTENING, waiting for state change")
                    self.condition.wait()
                    # Poll for message
                    # Parse data and call GUI to plot it
                    # In case of dropped connection, call GUI routine to stop plotting
                    # and display error message, then return to CONNECTED

        print("RUN end")


if __name__ == "__main__":
    fsm = SerialFSM(None, None)
    fsm.start()

    while True:
        fsm.set_state(FSMState.SYNC)
        time.sleep(5)
