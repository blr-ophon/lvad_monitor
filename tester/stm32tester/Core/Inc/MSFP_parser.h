#ifndef MSFP_PARSER_H
#define MSFP_PARSER_H

#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>

typedef enum{
    PKTTYPE_SYNC,
    PKTTYPE_SYNC_RESP,
    PKTTYPE_ACK,
    PKTTYPE_REQ,
    PKTTYPE_REQ_RESP,
    PKTTYPE_STOP,
} MSFP_PacketType;

typedef struct{
    MSFP_PacketType type;
    uint16_t data_size;
    uint16_t reserved;
    uint8_t *data;
    uint8_t EOM;
} MSFP_Packet;

int MSFP_ParseMsg(uint8_t *msg, int size, MSFP_Packet *packet);

#endif
