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
from msg_parser import MsgParse, MsgCommand


class FSMState(Enum):
    IDLE = 1
    SYNC = 2
    CONNECTED = 3
    LISTENING = 4
    
    def __str__(self):
        return self.name


class SerialFSM():
    """
    Finite state machine for serial connection
    """
    def __init__(self, serialCtrl, gui):
        self.state = FSMState.IDLE
        self.serialCtrl = serialCtrl

        self.thread = None
        self.change_state = threading.Condition()

        self.running = False
        self.received_packet = None

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

    def set_state(self, new_state):
        """
        Change FSM state
        """
        with self.change_state:
            print(f"{self.state} >> {new_state}")
            self.state = new_state
            # Wake up the thread waiting on this condition
            self.change_state.notify()

    def request_data(self, channels_n):
        """
        send REQUEST message with user specified number of channels
        """
        if self.state != FSMState.CONNECTED:
            print("Error: Not connected")
            return

        print(f"Requesting {channels_n} channels")
        self.set_state(FSMState.LISTENING)
        self.print_fsm_state(self.state)
        self.serialCtrl.send("#A#$")

    def stop_request(self):
        print("sending stop")
        self.serialCtrl.send("#S#$")
        print("stop sent")

    def run(self):
        """
        FSM loop
        """
        sync_timeout_start = False
        sync_timeout_start_time = 0

        while self.running:
            with self.change_state:

                if self.state == FSMState.IDLE:
                    # Do nothing. Wait for user/GUI to change this state
                    self.print_fsm_state(self.state)
                    self.change_state.wait()

                elif self.state == FSMState.SYNC:
                    self.print_fsm_state(self.state)

                    # Send sync packet
                    self.serialCtrl.send("#?#$")

                    # Poll for response
                    response = self.serialCtrl.listen()
                    time.sleep(0.5)
                    print(response)
                    continue

                    # Always check if fsm has not been stopped during blocking
                    # operation after it is done
                    if not self.running:
                        continue

                    # Parse and validate response
                    if response is not None:
                        self.received_packet = MsgParse(response)
                        if self.received_packet.command == MsgCommand.SYNC_RESP:
                            # Switch to connected
                            self.set_state(FSMState.CONNECTED)

                            #  Update GUI
                            self.gui.conn.status_connected(self.received_packet.channels_n)

                        else:
                            # TODO: improper, this does not handle the MCU not sending anything
                            # Try syncing until timeout
                            if not sync_timeout_start:
                                sync_timeout_start = True
                                sync_timeout_start_time = time.time()

                            if time.time() - sync_timeout_start_time > 3:
                                sync_timeout_start = False
                                print(">> SYNC failed")
                                # Return to IDLE
                                self.set_state(FSMState.IDLE)
                                #  Update GUI
                                self.gui.conn.status_failed()

                elif self.state == FSMState.CONNECTED:
                    self.print_fsm_state(self.state)

                    # TODO: keep connection alive through PING
                    # Do nothing. Wait for user prompt on GUI (Start Button)
                    self.change_state.wait()

                    # Send message to MCU
                    # Switch state to listening

                elif self.state == FSMState.LISTENING:
                    # Poll for message
                    response = self.serialCtrl.listen()
                    if response is not None:
                        print(response)
                        self.received_packet = MsgParse(response)
                        if self.received_packet.command == MsgCommand.STOP:
                            # Switch back to connected
                            print("STOP received")
                            self.set_state(FSMState.CONNECTED)
                    # Parse data and call GUI to plot it
                    # In case of dropped connection, call GUI routine to stop plotting
                    # and display error message, then return to CONNECTED

    @staticmethod
    def print_fsm_state(state):
        color = 34
        match state:
            case FSMState.IDLE:
                color = 34
            case FSMState.SYNC:
                color = 33
            case FSMState.CONNECTED:
                color = 31
            case FSMState.LISTENING:
                color = 92

        print(f"\033[{color}m[{state}]\033[0m")

if __name__ == "__main__":
    fsm = SerialFSM(None, None)
    fsm.start()

    while True:
        fsm.set_state(FSMState.SYNC)
        time.sleep(5)
