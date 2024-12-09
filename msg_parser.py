# Future:
# Parse MSFP messages
import re
from dataclasses import dataclass
from enum import Enum

class MsgCommand(Enum):
    SYNC = 1            # ?
    SYNC_RESP = 2       # !
    REQ = 3             # A
    REQ_RESP = 4        # D
    STOP = 5            # S

@dataclass
class parsedMsg:
    command: int
    channels_n: int





class MsgParser():
    def __init__(self):
        self.sync = "#?#$"
        self.sync_ok = "!"
        self.StartStream = "#A#$"
        self.StopStream = "#S#$"
        self.SyncChannel = 0

    def parse(self, msg):
        """
        Parse message to dataclass
        """
        tokens = self.split_msg(msg)
        parsed_msg = parsedMsg(None, None)

        match tokens[0]:
            case "?":
                parsed_msg.command = MsgCommand.SYNC
                parsed_msg = None
                print("Unexpected msg (SYNC)")

            case "!":
                parsed_msg.command = MsgCommand.SYNC_RESP
                parsed_msg.channels_n = int(tokens[1])

            case "A":
                parsed_msg.command = MsgCommand.REQ
                parsed_msg = None
                print("Unexpected msg (REQ)")

            case "D":
                parsed_msg.command = MsgCommand.REQ_RESP

            case "S":
                parsed_msg.command = MsgCommand.STOP
                parsed_msg = None
                print("Unexpected msg (STOP)")

        return parsed_msg

    def split_msg(self, msg):
        """
        Split message parts between separators
        """
        tmp_msg = msg.decode("utf-8")
        tmp_msg = tmp_msg.rstrip('$')
        tokens = re.findall(r'(?<=#)(.*?)(?=#)', tmp_msg)
        return tokens
