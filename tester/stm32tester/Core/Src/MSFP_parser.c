#include "MSFP_parser.h"

int MSFP_ParseMsg(uint8_t *msg, int size, MSFP_Packet *packet){
    int rv = 1;

    memset(packet, 0, sizeof(MSFP_Packet));
    
    char *msg_str = (char*) msg;
    char *pMsgStart = strchr(msg_str, '#');

    if(pMsgStart == NULL) {
        //No '#' found. Discard message
        rv = -1;
        goto out;
    }

    char opt = pMsgStart[1];
    switch(opt) {
        case '?':
            // SYNC
            packet->type = PKTTYPE_SYNC;
            break;
        case 'A':
            // REQ
            packet->type = PKTTYPE_REQ;
            break;
        case 'S':
            // STOP
            packet->type = PKTTYPE_STOP;
            break;
    }

out:
    return rv;
}
