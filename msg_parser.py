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
    channel1_data: float
    channel2_data: float


def MsgParse(raw_msg):
    """
    Parse message to dataclass
    """
    msg_tokens = tokenize_msg(raw_msg)
    if not msg_tokens:
        print(f"Invalid Message: {raw_msg}")
        return None
    parsed_msg = parsedMsg(None, None, None, None)

    match msg_tokens[0]:
        case "?":
            parsed_msg.command = MsgCommand.SYNC
            parsed_msg = None
            print("Unexpected msg (SYNC)")

        case "!":
            parsed_msg.command = MsgCommand.SYNC_RESP
            parsed_msg.channels_n = int(msg_tokens[1])

        case "A":
            parsed_msg.command = MsgCommand.REQ
            parsed_msg = None
            print("Unexpected msg (REQ)")

        case "D":
            parsed_msg.command = MsgCommand.REQ_RESP
            parsed_msg.channel1_data = msg_tokens[1]
            parsed_msg.channel2_data = msg_tokens[2]

        case "S":
            parsed_msg.command = MsgCommand.STOP

    return parsed_msg

def tokenize_msg(msg):
    """
    Split message parts between separators
    """
    tmp_msg = msg.decode("utf-8")
    tmp_msg = tmp_msg.rstrip('$')
    tokens = re.findall(r'(?<=#)(.*?)(?=#)', tmp_msg)
    return tokens
